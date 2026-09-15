from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in first.", "error")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

def redirect_if_logged_in(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" in session:
            return redirect(url_for("bit.bit"))
        return f(*args, **kwargs)
    return decorated