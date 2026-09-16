from flask import Blueprint, render_template
from auth import login_required, admin_required

bit_bp = Blueprint(
    "bit", __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/bit/static"
)


@bit_bp.route("/8-bit")
@login_required
def bit():
    return render_template("bit.html")


@bit_bp.route("/8-bit/vending-machine")
@login_required
def vending_machine():
    return render_template("vending_machine.html")


@bit_bp.route("/8-bit/games")
@login_required
def games():
    return render_template("games.html")


@bit_bp.route("/8-bit/dashboard")
@admin_required
def dashboard():
    return render_template("dashboard.html")