import random
from flask import Blueprint, render_template, request, session, jsonify
from auth import login_required
import os
from flask import send_from_directory

race_bp = Blueprint(
    "race", __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/bit/games/race/static"   # unique, doesn't collide with bit_bp's "/bit/static"
)
# remove the manual race_static route + RACE_STATIC_DIR — not needed anymore

WIN_REWARD = 300
RACER_ORDER = ["yellow", "red", "purple", "blue", "green", "black"]
FINISH = 100  # abstract finish line; frontend maps 0..FINISH onto its own pixel track
MAX_TICKS = 500  # safety cap so a freak run can't loop forever


# --- TODO: replace these two with your real DB calls, keyed by user_id ---
# Whatever you use (SQLAlchemy model, raw SQL, etc.), these are the only two
# functions the route below needs -- swap the bodies, keep the signatures.
def get_coins(user_id):
    session.setdefault("coins", 0)
    return session["coins"]


def add_coins(user_id, amount):
    session.setdefault("coins", 0)
    session["coins"] += amount
    return session["coins"]
# ---------------------------------------------------------------------


def simulate_race():
    """Runs the whole race server-side and returns every frame plus the winner.
    Same random-walk logic the old client-side JS used, just moved here so the
    server is the one and only source of truth for who won."""
    positions = {c: 0.0 for c in RACER_ORDER}
    frames = []
    winner = None

    for _ in range(MAX_TICKS):
        step = {}
        for c in RACER_ORDER:
            positions[c] += random.uniform(0, 3)
            step[c] = round(positions[c], 2)
            if winner is None and positions[c] >= FINISH:
                winner = c
        frames.append(step)
        if winner:
            break

    if winner is None:
        # extremely unlikely safety net: whoever's furthest along wins
        winner = max(positions, key=positions.get)

    return frames, winner


@race_bp.route("/8-bit/games/race")
@login_required
def race():
    coins = get_coins(session["user_id"])
    return render_template("race.html", coins=coins)


@race_bp.route("/8-bit/games/race/api/race", methods=["POST"])
@login_required
def run_race():
    data = request.get_json(silent=True) or {}
    prediction = data.get("prediction")
    if prediction not in RACER_ORDER:
        return jsonify({"error": "invalid prediction"}), 400

    frames, winner = simulate_race()
    won = prediction == winner

    awarded = 0
    if won:
        awarded = WIN_REWARD
        add_coins(session["user_id"], WIN_REWARD)

    return jsonify({
        "frames": frames,
        "finish": FINISH,
        "winner": winner,
        "won": won,
        "awarded": awarded,
        "coins": get_coins(session["user_id"]),
    })