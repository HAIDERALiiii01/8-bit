from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
import os
import re
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

from auth import login_required, redirect_if_logged_in
from bit.bit import bit_bp

load_dotenv()

password = os.getenv("PASSWORD")

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://postgres:{password}@localhost/vending_machine"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
limiter = Limiter(get_remote_address, app=app, default_limits=[])

app.register_blueprint(bit_bp)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)


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
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = user.username
            flash("Login successful!", "info")
            return redirect(url_for("bit.bit"))
        else:
            flash("Invalid username or password", "error")

    return render_template("login.html")


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
        password = request.form.get("password")
        age = request.form.get("age")
        gender = request.form.get("gender", "").strip().lower()

        if not username or not email or not password or not age or not gender:
            flash("Please fill in all the details.", "error")
            return redirect(url_for("register"))

        if len(username) > 100 or len(email) > 100:
            flash("Username or email is too long.", "error")
            return redirect(url_for("register"))

        if not re.match(r"^[^@\s]+@gmail\.com$", email):
            flash("Enter a valid Gmail address.", "error")
            return redirect(url_for("register"))

        if len(password) < 8:
            flash("Password must be at least 8 characters.", "error")
            return redirect(url_for("register"))

        if not re.search(r"[A-Za-z]", password) or not re.search(r"\d", password) or not re.search(r"[^A-Za-z0-9]", password):
            flash("Password must contain letters, numbers, and a special character.", "error")
            return redirect(url_for("register"))

        try:
            age = int(age)
        except ValueError:
            flash("Age must be a number", "error")
            return redirect(url_for("register"))

        if age < 13 or age > 120:
            flash("Age must be between 13 and 120", "error")
            return redirect(url_for("register"))

        if gender not in ("male", "female"):
            flash("Invalid gender selection", "error")
            return redirect(url_for("register"))

        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        if existing_user:
            flash("Username or email already registered", "error")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)
        user = User(username=username, email=email, password=hashed_password, age=age, gender=gender)
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Username or email already registered", "error")
            return redirect(url_for("register"))

        flash("Registration successful!", "info")
        return redirect(url_for("login"))

    return render_template("register.html")


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)