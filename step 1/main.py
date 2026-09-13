from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

password = os.getenv("PASSWORD")

# print(password)

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://postgres:{password}@localhost/vending_machine"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
@app.route("/add-user")
def add_user():
    user = User(
        username="haider",
        email="haider@gmail.com",
        password="12345"
    )

    db.session.add(user)
    db.session.commit()

    return "User added successfully!"

@app.route("/")
def home():
    return "<h1>Flask + PostgreSQL is working!</h1>"

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            return "Login successful!"

        return "Invalid username or password!"

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        user = User(
            username=username,
            email=email,
            password=password
        )

        db.session.add(user)
        db.session.commit()

        return "Registration successful!"

    return render_template("register.html")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)