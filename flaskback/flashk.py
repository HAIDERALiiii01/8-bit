from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from admin.second import second

app = Flask(__name__)
app.register_blueprint(second, url_prefix="/admin")
app.secret_key = "hello"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=3)

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    
    def __init__(self, name, email):
        self.name = name
        self.email = email
         

# Defining the home page of our site
@app.route("/home")  # this sets the route to this page
@app.route("/")  # this sets the route to this page
def home():
	return render_template("index.html")

@app.route("/view")
def view():
	return render_template("view.html", values=users.query.all())

@app.route("/delete")
def delete():
    found_user = users.query.filter_by(name="haider").first()
    if found_user:
        db.session.delete(found_user)
        db.session.commit()
    return render_template("view.html", values=users.query.all())



@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]
        
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            flash("Email was saved")
            
        
        else:
            if "email" in session:
                email = session["email"]
        
        return render_template("user.html", email=email, user=user)
    else:
        flash("You are not logged in")
        return redirect(url_for("login"))
    
@app.route("/admin0")
def admin():
	return redirect(url_for("user", usr="haider!")) 

@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"You have been logged out! {user}", "info")
    session.pop("user", None)
    session.pop("email", None)    
    return redirect(url_for("login"))

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True  # <--- makes the permanent session
        user = request.form["nm"]
        session["user"] = user
        
        found_user = users.query.filter_by(name=user).first()
        if found_user:
            session["email"] = found_user.email
        else:
            usr = users(user, "")
            db.session.add(usr)
            db.session.commit()
        
        flash("Login Successful!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already Logged in")
            return redirect(url_for("user"))

        return render_template("login.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
    app.run(debug=True)