from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from sqlalchemy import func
from extensions import db
from models import Game, GameSessions, CoinTransactions, Orders, OrderItems, Products

KARACHI = ZoneInfo("Asia/Karachi")
PLAYS_PER_GAME_PER_DAY = 3
EXTRA_BIT_PRODUCT_NAME = "Extra Bit"  # must match Products.product_name exactly


def day_start_utc():
    """Karachi midnight today, as a naive UTC datetime (matches how played_at is stored)."""
    now_khi = datetime.now(KARACHI)
    midnight = now_khi.replace(hour=0, minute=0, second=0, microsecond=0)
    return midnight.astimezone(timezone.utc).replace(tzinfo=None)


def get_game(game_name):
    return Game.query.filter_by(game_name=game_name).first()


def extra_lives_today(user_id):
    """How many Extra Bit units the user has bought today (each unit = +1 play,
    applied to every game). Counts quantity, not just purchase count, so
    buying 2 in one order grants +2."""
    total = (
        db.session.query(func.coalesce(func.sum(OrderItems.quantity), 0))
        .join(Orders, OrderItems.order_id == Orders.order_id)
        .join(Products, OrderItems.product_id == Products.product_id)
        .filter(
            Orders.user_id == user_id,
            Orders.purchased_at >= day_start_utc(),
            Products.product_name == EXTRA_BIT_PRODUCT_NAME,
        )
        .scalar()
    )
    return int(total)


def plays_left(user_id, game_name):
    used = GameSessions.query.filter(
        GameSessions.user_id == user_id,
        GameSessions.game_id == get_game(game_name).game_id,
        GameSessions.played_at >= day_start_utc(),
    ).count()
    bonus = extra_lives_today(user_id)
    return max(0, PLAYS_PER_GAME_PER_DAY + bonus - used)


def get_coins(user_id):
    """Balance = sum of the ledger (your ER notes say not to store a balance)."""
    total = db.session.query(
        func.coalesce(func.sum(CoinTransactions.amount), 0)
    ).filter(CoinTransactions.user_id == user_id).scalar()
    return int(total)


def get_high_score(user_id, game_name):
    best = db.session.query(func.max(GameSessions.score)).filter(
        GameSessions.user_id == user_id,
        GameSessions.game_id == get_game(game_name).game_id,
    ).scalar()
    return best or 0


def record_play(user_id, game_name, score, coins_earned):
    """Uses up one play: session row + coin ledger row, in ONE commit.
    Returns the new coin balance, or None if the user had no plays left."""
    if plays_left(user_id, game_name) == 0:
        return None
    db.session.add(GameSessions(
        user_id=user_id, game_id=get_game(game_name).game_id,
        score=score, coins_earned=coins_earned,
    ))
    if coins_earned > 0:
        db.session.add(CoinTransactions(
            user_id=user_id, amount=coins_earned, transaction_type="game_reward",
        ))
    db.session.commit()
    return get_coins(user_id)