import logging
from flask import render_template, session, request, jsonify
from auth import login_required
from extensions import db
from models import Products, Orders, OrderItems, CoinTransactions, User
from bit.games.game import get_coins
from bit.mail import send_receipt_email


def register_vending_routes(bit_bp):

    @bit_bp.route("/8-bit/vending-machine")
    @login_required
    def vending_machine():
        products = (
            Products.query
            .filter(Products.status == "active")
            .order_by(Products.category, Products.product_name)
            .all()
        )
        uid = session["user_id"]
        return render_template(
            "vending_machine.html",
            products=products,
            total_coins=get_coins(uid),
        )

    @bit_bp.route("/8-bit/vending-machine/checkout", methods=["POST"])
    @login_required
    def checkout():
        uid = session["user_id"]
        data = request.get_json(silent=True) or {}
        raw_cart = data.get("cart", {})

        if not raw_cart:
            return jsonify(ok=False, error="Your tray is empty."), 400

        try:
            items = {int(pid): int(qty) for pid, qty in raw_cart.items() if int(qty) > 0}
        except (TypeError, ValueError):
            return jsonify(ok=False, error="Bad cart data."), 400

        if not items:
            return jsonify(ok=False, error="Your tray is empty."), 400

        products = Products.query.filter(Products.product_id.in_(items.keys())).all()
        products_by_id = {p.product_id: p for p in products}

        total = 0
        for pid, qty in items.items():
            product = products_by_id.get(pid)
            if not product or product.status != "active":
                return jsonify(ok=False, error="One of those items is no longer available."), 400
            if qty > product.stock_quantity:
                return jsonify(ok=False, error=f"Only {product.stock_quantity} left of {product.product_name}."), 400
            total += product.price * qty

        coins = get_coins(uid)
        if total > coins:
            return jsonify(ok=False, error="Not enough coins."), 400

        order = Orders(user_id=uid, total_amount=total, payment_status="completed")
        db.session.add(order)
        db.session.flush()

        for pid, qty in items.items():
            product = products_by_id[pid]
            db.session.add(OrderItems(
                order_id=order.order_id,
                product_id=pid,
                quantity=qty,
                unit_price=product.price,
                subtotal=product.price * qty,
            ))
            product.stock_quantity -= qty

        db.session.add(CoinTransactions(
            user_id=uid,
            amount=-total,
            transaction_type="vending_purchase",
        ))

        db.session.commit()

        # Email the receipt. This runs after commit, so a failure here never
        # rolls back a completed purchase -- coins are already spent and
        # stock already decremented. We just log it and let the purchase
        # succeed from the user's point of view.
        user = User.query.get(uid)
        try:
            send_receipt_email(user, order)
        except Exception:
            logging.exception("Failed to send receipt email for order %s", order.order_id)

        return jsonify(ok=True, new_balance=get_coins(uid), order_id=order.order_id)