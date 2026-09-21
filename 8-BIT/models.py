from datetime import datetime, timezone
from extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    # One user -> many game sessions. Deleting a user deletes their sessions.
    sessions = db.relationship(
        "GameSessions", back_populates="user", cascade="all, delete-orphan"
    )

    # One user -> many coin transactions. Deleting a user deletes their transaction history.
    transactions = db.relationship(
        "CoinTransactions", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.username}>"


class Game(db.Model):
    __tablename__ = "games"

    game_id = db.Column(db.Integer, primary_key=True)
    game_name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    coin_reward = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, default=True, nullable=False)

    # One game -> many game sessions.
    sessions = db.relationship("GameSessions", back_populates="game")

    def __repr__(self):
        return f"<Game {self.game_name}>"


class GameSessions(db.Model):
    __tablename__ = "gamesession"

    session_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey("games.game_id"), nullable=False)
    score = db.Column(db.Integer, nullable=False, default=0)
    coins_earned = db.Column(db.Integer, nullable=False, default=0)
    played_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    # Many sessions -> one user / one game.
    user = db.relationship("User", back_populates="sessions")
    game = db.relationship("Game", back_populates="sessions")

    def __repr__(self):
        return f"<GameSession {self.session_id} user={self.user_id} game={self.game_id}>"
    
    
class CoinTransactions(db.Model):
    __tablename__ = "cointransactions"

    transaction_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    # Many transactions -> one user.
    user = db.relationship("User", back_populates="transactions")

    def __repr__(self):
        return f"<CoinTransaction {self.transaction_id} user={self.user_id} amount={self.amount}>"