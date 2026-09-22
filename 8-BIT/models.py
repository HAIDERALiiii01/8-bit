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

    # One user -> many orders. Deleting a user deletes their orders.
    orders = db.relationship(
        "Orders", back_populates="user", cascade="all, delete-orphan"
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


class Orders(db.Model):
    __tablename__ = "orders"

    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    total_amount = db.Column(db.Integer, nullable=False)
    payment_status = db.Column(db.String(50), nullable=False)
    purchased_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    # Many orders -> one user.
    user = db.relationship("User", back_populates="orders")

    # One order -> many order items. Deleting an order deletes its items.
    items = db.relationship(
        "OrderItems", back_populates="order", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Order {self.order_id} user={self.user_id} total={self.total_amount}>"


class OrderItems(db.Model):
    __tablename__ = "orderitems"

    order_item_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.order_id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.product_id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Integer, nullable=False)

    # Many order items -> one order / one product.
    order = db.relationship("Orders", back_populates="items")
    product = db.relationship("Products", back_populates="order_items")

    def __repr__(self):
        return f"<OrderItem {self.order_item_id} order={self.order_id} product={self.product_id}>"


class Products(db.Model):
    __tablename__ = "products"

    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False)

    # One product -> many order items.
    order_items = db.relationship("OrderItems", back_populates="product")

    def __repr__(self):
        return f"<Product {self.product_id} name={self.product_name}>"