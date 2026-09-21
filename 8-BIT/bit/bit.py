from flask import Blueprint, render_template, session
from auth import login_required, admin_required
from bit.games.race.race import race_bp
from bit.games.snake.snake import snake_bp
from bit.games.game import PLAYS_PER_GAME_PER_DAY, get_coins, plays_left

bit_bp = Blueprint(
    "bit", __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/bit/static"
)
bit_bp.register_blueprint(race_bp)
bit_bp.register_blueprint(snake_bp)


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
    uid = session["user_id"]
    return render_template("games.html", coins=get_coins(uid),
                           race_lives=plays_left(uid, "Turtle Race"),
                           snake_lives=plays_left(uid, "Snake"),
                           max_lives=PLAYS_PER_GAME_PER_DAY)


@bit_bp.route("/8-bit/dashboard")
@admin_required
def dashboard():
    return render_template("dashboard.html")