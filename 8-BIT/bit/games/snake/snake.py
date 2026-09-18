from flask import Blueprint, render_template, request, session, jsonify
from auth import login_required
import os
from flask import send_from_directory
# NOTE on static_url_path: race.py uses "/bit/static" for its own blueprint.
# Since each game blueprint typically lives in its own folder with its own
# "static" subfolder, giving snake a DIFFERENT static_url_path avoids two
# blueprints registering the same literal URL rule under the parent "bit"
# blueprint. Adjust to match however your project actually nests these.
snake_bp = Blueprint(
    "snake", __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/bit/games/snake/static"   # unique too
)
# remove the manual snake_static route + SNAKE_STATIC_DIR

COINS_PER_FOOD = 10
GRID_COUNT = 28          # must match GRID_COUNT in snake.html
MAX_REASONABLE_SCORE = GRID_COUNT * GRID_COUNT  # can't eat more food than cells on the board


# --- TODO: replace these four with your real DB calls, keyed by user_id ---
# Same pattern as race.py -- swap the bodies, keep the signatures.
def get_coins(user_id):
    session.setdefault("coins", 0)
    return session["coins"]


def add_coins(user_id, amount):
    session.setdefault("coins", 0)
    session["coins"] += amount
    return session["coins"]


def get_high_score(user_id):
    session.setdefault("snake_high_score", 0)
    return session["snake_high_score"]


def set_high_score(user_id, score):
    session["snake_high_score"] = score
    return score
# ---------------------------------------------------------------------


@snake_bp.route("/8-bit/games/snake")
@login_required
def snake():
    coins = get_coins(session["user_id"])
    high_score = get_high_score(session["user_id"])
    return render_template("snake.html", coins=coins, high_score=high_score)


@snake_bp.route("/8-bit/games/snake/api/finish", methods=["POST"])
@login_required
def finish_run():
    """The browser plays the actual game (it's real-time, unlike the race's
    server-simulated frames) and reports the final score here. The server
    is still the one deciding coins and high score, so a tampered client
    can't just hand itself coins."""
    data = request.get_json(silent=True) or {}
    score = data.get("score")

    if not isinstance(score, int) or score < 0 or score > MAX_REASONABLE_SCORE:
        return jsonify({"error": "invalid score"}), 400

    awarded = score * COINS_PER_FOOD
    if awarded > 0:
        add_coins(session["user_id"], awarded)

    high_score = get_high_score(session["user_id"])
    new_high_score = False
    if score > high_score:
        high_score = set_high_score(session["user_id"], score)
        new_high_score = True

    return jsonify({
        "awarded": awarded,
        "coins": get_coins(session["user_id"]),
        "high_score": high_score,
        "new_high_score": new_high_score,
    })