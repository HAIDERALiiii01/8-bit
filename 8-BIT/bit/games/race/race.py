import random

from flask import Blueprint, render_template, request, session, jsonify

from auth import login_required
from bit.games.game import PLAYS_PER_GAME_PER_DAY, get_coins, get_game, plays_left, record_play

race_bp = Blueprint(
    "race", __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/bit/games/race/static",
)

GAME_NAME = "Turtle Race"   # must match seed_games()
RACER_ORDER = ["yellow", "red", "purple", "blue", "green", "black"]
FINISH = 100      # abstract finish line; the frontend maps 0..FINISH onto its pixel track
MAX_TICKS = 500   # safety cap so a freak run can't loop forever


def simulate_race():
    """Runs the whole race server-side and returns every frame plus the winner."""
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
        winner = max(positions, key=positions.get)  # extremely unlikely safety net

    return frames, winner


@race_bp.route("/8-bit/games/race")
@login_required
def race():
    uid = session["user_id"]
    return render_template("race.html", coins=get_coins(uid),
                       plays_left=plays_left(uid, GAME_NAME),
                       max_lives=PLAYS_PER_GAME_PER_DAY)


@race_bp.route("/8-bit/games/race/api/race", methods=["POST"])
@login_required
def run_race():
    uid = session["user_id"]
    data = request.get_json(silent=True) or {}
    prediction = data.get("prediction")
    if prediction not in RACER_ORDER:
        return jsonify({"error": "invalid prediction"}), 400

    if plays_left(uid, GAME_NAME) == 0:
        return jsonify({"error": "no plays left today"}), 403

    frames, winner = simulate_race()
    won = prediction == winner
    awarded = get_game(GAME_NAME).coin_reward if won else 0

    # score=int(won) is a placeholder: a race has no natural score
    coins = record_play(uid, GAME_NAME, score=int(won), coins_earned=awarded)
    if coins is None:  # lost a race between the check above and the save
        return jsonify({"error": "no plays left today"}), 403

    return jsonify({
        "frames": frames,
        "finish": FINISH,
        "winner": winner,
        "won": won,
        "awarded": awarded,
        "coins": coins,
        "plays_left": plays_left(uid, GAME_NAME),
    })