"""
Admin dashboard routes for the `bit` blueprint.

Wired up the same way vending_machine.py is: this module exposes
`register_dashboard_routes(bp)`, which attaches every route directly onto
whatever blueprint you pass it. In bit.py:

    from bit.dashboard import register_dashboard_routes
    ...
    register_dashboard_routes(bit_bp)

right next to the existing `register_vending_routes(bit_bp)` call. That's
what makes `url_for('bit.dashboard')` resolve — these aren't a nested
sub-blueprint (like race/snake), they live directly on bit_bp, matching
how vending_machine's routes do.

Routes are full paths (no blueprint url_prefix is used anywhere else in
bit.py), so everything here is rooted at /8-bit/dashboard to match that.
"""

from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from flask import render_template, request, redirect, url_for, flash
from sqlalchemy import func

from auth import login_required, admin_required
from extensions import db
from models import User, Game, GameSessions, CoinTransactions, Orders, Products

KARACHI_TZ = ZoneInfo("Asia/Karachi")


def _today_start_utc():
    """Midnight in Karachi, converted to UTC."""
    now_karachi = datetime.now(KARACHI_TZ)
    midnight_karachi = now_karachi.replace(hour=0, minute=0, second=0, microsecond=0)
    return midnight_karachi.astimezone(timezone.utc)


def _coin_sum(*filters):
    """Sum of CoinTransactions.amount matching the given filter expressions (0 if none)."""
    return db.session.query(func.coalesce(func.sum(CoinTransactions.amount), 0)).filter(*filters).scalar()


def register_dashboard_routes(bp):

    @bp.route("/8-bit/dashboard")
    @login_required
    @admin_required
    def dashboard():
        today_start = _today_start_utc()

        stats = {
            "total_players": User.query.count(),
            "sessions_total": GameSessions.query.count(),
            "sessions_today": GameSessions.query.filter(GameSessions.played_at >= today_start).count(),
            "players_today": (
                db.session.query(func.count(func.distinct(GameSessions.user_id)))
                .filter(GameSessions.played_at >= today_start)
                .scalar()
            ),
            "coins_earned_total": _coin_sum(CoinTransactions.amount > 0),
            "coins_spent_total": abs(_coin_sum(CoinTransactions.amount < 0)),
            "coins_earned_today": _coin_sum(
                CoinTransactions.amount > 0, CoinTransactions.created_at >= today_start
            ),
            "coins_spent_today": abs(
                _coin_sum(CoinTransactions.amount < 0, CoinTransactions.created_at >= today_start)
            ),
            "coins_in_circulation": _coin_sum(),  # net balance across every user: earned minus spent
            "pending_orders": Orders.query.filter_by(payment_status="pending").count(),
        }

        games = Game.query.order_by(Game.game_id).all()
        game_play_counts = dict(
            db.session.query(GameSessions.game_id, func.count(GameSessions.session_id))
            .group_by(GameSessions.game_id)
            .all()
        )

        products = Products.query.order_by(Products.product_id).all()

        search = request.args.get("q", "").strip()
        users_query = User.query
        if search:
            like = f"%{search}%"
            users_query = users_query.filter((User.username.ilike(like)) | (User.email.ilike(like)))
        users = users_query.order_by(User.id).all()

        balances_by_user = dict(
            db.session.query(CoinTransactions.user_id, func.coalesce(func.sum(CoinTransactions.amount), 0))
            .group_by(CoinTransactions.user_id)
            .all()
        )
        sessions_by_user = dict(
            db.session.query(GameSessions.user_id, func.count(GameSessions.session_id))
            .group_by(GameSessions.user_id)
            .all()
        )

        return render_template(
            "dashboard.html",
            stats=stats,
            games=games,
            game_play_counts=game_play_counts,
            products=products,
            users=users,
            search=search,
            balances_by_user=balances_by_user,
            sessions_by_user=sessions_by_user,
        )

    @bp.route("/8-bit/dashboard/game/<int:game_id>/toggle", methods=["POST"])
    @login_required
    @admin_required
    def toggle_game(game_id):
        game = Game.query.get_or_404(game_id)
        game.status = not game.status
        db.session.commit()
        flash(f"{game.game_name} {'enabled' if game.status else 'disabled'}.", "info")
        return redirect(url_for("bit.dashboard"))

    @bp.route("/8-bit/dashboard/game/<int:game_id>/reward", methods=["POST"])
    @login_required
    @admin_required
    def update_game_reward(game_id):
        game = Game.query.get_or_404(game_id)
        raw = request.form.get("coin_reward", "").strip()

        try:
            reward = int(raw)
        except ValueError:
            flash("Coin reward must be a whole number.", "error")
            return redirect(url_for("bit.dashboard"))

        if reward < 0:
            flash("Coin reward can't be negative.", "error")
            return redirect(url_for("bit.dashboard"))

        game.coin_reward = reward
        db.session.commit()
        flash(f"{game.game_name} reward set to {reward} coins.", "info")
        return redirect(url_for("bit.dashboard"))

    @bp.route("/8-bit/dashboard/product/<int:product_id>/toggle", methods=["POST"])
    @login_required
    @admin_required
    def toggle_product(product_id):
        product = Products.query.get_or_404(product_id)
        product.status = "out_of_stock" if product.status == "active" else "active"
        db.session.commit()
        flash(f"{product.product_name} marked {product.status.replace('_', ' ')}.", "info")
        return redirect(url_for("bit.dashboard"))

    @bp.route("/8-bit/dashboard/product/<int:product_id>/update", methods=["POST"])
    @login_required
    @admin_required
    def update_product(product_id):
        product = Products.query.get_or_404(product_id)

        try:
            price = int(request.form.get("price", "").strip())
            stock = int(request.form.get("stock_quantity", "").strip())
        except ValueError:
            flash("Price and stock must be whole numbers.", "error")
            return redirect(url_for("bit.dashboard"))

        if price < 0 or stock < 0:
            flash("Price and stock can't be negative.", "error")
            return redirect(url_for("bit.dashboard"))

        product.price = price
        product.stock_quantity = stock
        db.session.commit()
        flash(f"{product.product_name} updated.", "info")
        return redirect(url_for("bit.dashboard"))

    @bp.route("/8-bit/dashboard/user/<int:user_id>")
    @login_required
    @admin_required
    def user_detail(user_id):
        user = User.query.get_or_404(user_id)

        sessions = (
            GameSessions.query.filter_by(user_id=user.id)
            .order_by(GameSessions.played_at.desc())
            .limit(50)
            .all()
        )
        orders = Orders.query.filter_by(user_id=user.id).order_by(Orders.purchased_at.desc()).all()
        transactions = (
            CoinTransactions.query.filter_by(user_id=user.id)
            .order_by(CoinTransactions.created_at.desc())
            .limit(50)
            .all()
        )

        balance = _coin_sum(CoinTransactions.user_id == user.id)
        total_sessions = GameSessions.query.filter_by(user_id=user.id).count()
        total_spent = abs(_coin_sum(CoinTransactions.user_id == user.id, CoinTransactions.amount < 0))

        return render_template(
            "dashboard_user.html",
            user=user,
            sessions=sessions,
            orders=orders,
            transactions=transactions,
            balance=balance,
            total_sessions=total_sessions,
            total_spent=total_spent,
        )