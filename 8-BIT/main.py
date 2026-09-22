import os
import re
from datetime import timedelta
from dotenv import load_dotenv
from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf import CSRFProtect
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from auth import login_required, redirect_if_logged_in
from bit.bit import bit_bp
from bit.games.game import get_coins
from extensions import db
from models import User, Game, GameSessions, Products  # importing registers the tables


load_dotenv()

db_password = os.getenv("PASSWORD")

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://postgres:{db_password}@localhost/vending_machine"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=30)

db.init_app(app)
csrf = CSRFProtect(app)
limiter = Limiter(get_remote_address, app=app, default_limits=[])

app.register_blueprint(bit_bp)


@app.route("/home")
@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("bit.bit"))
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
@redirect_if_logged_in
@limiter.limit("5 per minute")
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session.permanent = True  # <--- makes the permanent session
            session["user_id"] = user.id
            session["username"] = user.username
            session["is_admin"] = user.is_admin
            flash("Login successful!", "info")
            return redirect(url_for("bit.bit"))

        flash("Invalid username or password", "error")
        # Keep the username so the user only retypes the password.
        return render_template("login.html", form={"username": username})

    return render_template("login.html", form={})


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
@redirect_if_logged_in
@limiter.limit("5 per minute")
def register():

    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        age = request.form.get("age", "").strip()
        gender = request.form.get("gender", "").strip().lower()

        # Everything except the password is sent back to re-fill the form.
        form = {
            "username": username,
            "email": email,
            "age": age,
            "gender": gender,
        }

        def fail(message):
            flash(message, "error")
            return render_template("register.html", form=form)

        if not username or not email or not password or not age or not gender:
            return fail("Please fill in all the details.")

        if len(username) < 3 or len(username) > 20:
            return fail("Username must be between 3 and 20 characters.")

        if len(email) > 100:
            return fail("Email is too long.")

        if not re.match(r"^[^@\s]+@gmail\.com$", email):
            return fail("Enter a valid Gmail address.")

        if len(password) < 8:
            return fail("Password must be at least 8 characters.")

        if not re.search(r"[A-Za-z]", password) or not re.search(r"\d", password) or not re.search(r"[^A-Za-z0-9]", password):
            return fail("Password must contain letters, numbers, and a special character.")

        try:
            age = int(age)
        except ValueError:
            return fail("Age must be a number")

        if age < 13 or age > 120:
            return fail("Age must be between 13 and 120")

        if gender not in ("male", "female"):
            return fail("Invalid gender selection")

        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        if existing_user:
            return fail("Username or email already registered")

        hashed_password = generate_password_hash(password)
        user = User(username=username, email=email, password=hashed_password, age=age, gender=gender)
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return fail("Username or email already registered")

        flash("Registration successful!", "info")
        return redirect(url_for("login"))

    return render_template("register.html", form={})


def seed_games():
    games = [
        # (name, description, coin_reward)
        ("Snake", "Classic snake game", 50),                              # coins per 500 points
        ("Turtle Race", "Race your turtle to the finish line", 50),       # coins for a win
    ]
    for name, desc, reward in games:
        if not Game.query.filter_by(game_name=name).first():
            db.session.add(Game(game_name=name, description=desc, coin_reward=reward))
    db.session.commit()


def seed_products():
    products = [
        # (name, category, price, description)
        ("Chai", "Hot Drinks", 30,
        "A warm, comforting cup of traditional Pakistani tea, perfect for a quick refresh."),

        ("Coffee", "Hot Drinks", 50,
        "A hot, energizing coffee for a quick boost during your break or gaming session."),

        ("Pakola", "Drinks", 40,
        "A chilled, fizzy Pakistani classic with its signature sweet and refreshing taste."),

        ("Coke", "Drinks", 50,
        "A cold and refreshing cola to pair perfectly with your favorite snack."),

        ("Lays", "Snacks", 40,
        "Crispy and crunchy potato chips, perfect for a quick snack while you play."),

        ("Snickers", "Snacks", 50,
        "A chocolate bar packed with caramel, peanuts, nougat, and chocolate for a sweet energy boost."),

        ("Extra Bit", "Game", 60,
        "Get an extra Bit to keep playing your favorite games when you run out."),

        ("Egg Sandwich", "Food", 100,
        "A filling sandwich with a tasty egg filling, perfect for a quick and satisfying bite."),
    ]
    for name, category, price, description in products:
        if not Products.query.filter_by(product_name=name).first():
            db.session.add(Products(
                product_name=name,
                category=category,
                price=price,
                stock_quantity=50,
                description=description,
                status="active",
            ))
    db.session.commit()


@app.context_processor
def inject_total_coins():
    uid = session.get("user_id")
    return {"total_coins": get_coins(uid) if uid else None}

with app.app_context():
    db.create_all()
    seed_games()
    seed_products()


if __name__ == "__main__":
    app.run(debug=True)