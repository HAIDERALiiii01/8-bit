from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

load_dotenv()

password = os.getenv("PASSWORD")

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://postgres:{password}@localhost/vending_machine"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    

@app.route("/home")
@app.route("/")
def home():
    return render_template("home.html")

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in first.", "error")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


@app.route("/8-bit")
@login_required
def bit():
    return render_template("bit.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if "user_id" in session:
        flash("You are already logged in.", "info")
        return redirect(url_for("bit"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = user.username
            flash("Login successful!", "info")
            return redirect(url_for("bit"))
        else:
            flash("Invalid username or password", "error")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():

        if request.method == "POST":
            username = request.form.get("username")
            email = request.form.get("email")
            password = request.form.get("password")
            age = request.form.get("age")
            gender = request.form.get("gender")

            if not username or not email or not password or not age or not gender:
                flash("Please fill in all the details.", "error")
                return redirect(url_for("register"))

            if not email.endswith("@gmail.com"):
                flash("Only Gmail addresses are allowed.", "error")
                return redirect(url_for("register"))

            if len(password) < 8:
                flash("Password must be at least 8 characters.", "error")
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
                return redirect(url_for("register"))   # <-- was missing

            hashed_password = generate_password_hash(password)
            user = User(username=username, email=email, password=hashed_password, age=age, gender=gender)
            db.session.add(user)
            db.session.commit()

            flash("Registration successful!", "info")   # <-- was `return flash(...)`
            return redirect(url_for("login"))

        return render_template("register.html")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)