from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from sqlalchemy import func
from extensions import db
from models import Game, GameSessions, CoinTransactions # adjust the name to your model

KARACHI = ZoneInfo("Asia/Karachi")
PLAYS_PER_GAME_PER_DAY = 3


def day_start_utc():
    """Karachi midnight today, as a naive UTC datetime (matches how played_at is stored)."""
    now_khi = datetime.now(KARACHI)
    midnight = now_khi.replace(hour=0, minute=0, second=0, microsecond=0)
    return midnight.astimezone(timezone.utc).replace(tzinfo=None)


def get_game(game_name):
    return Game.query.filter_by(game_name=game_name).first()


def plays_left(user_id, game_name):
    used = GameSessions.query.filter(
        GameSessions.user_id == user_id,
        GameSessions.game_id == get_game(game_name).game_id,
        GameSessions.played_at >= day_start_utc(),
    ).count()
    return max(0, PLAYS_PER_GAME_PER_DAY - used)


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