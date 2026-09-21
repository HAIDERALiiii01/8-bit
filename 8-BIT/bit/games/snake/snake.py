from flask import Blueprint, render_template, request, session, jsonify

from auth import login_required
from bit.games.game import PLAYS_PER_GAME_PER_DAY, get_coins, get_game, get_high_score, plays_left, record_play

snake_bp = Blueprint(
    "snake", __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/bit/games/snake/static",
)

GAME_NAME = "Snake"   # must match seed_games()
GRID_COUNT = 28       # must match GRID_COUNT in snake.html
POINTS_PER_FOOD = 10  # must match the score increment in snake.html
SCORE_STEP = 500      # every full 500 points earns one coin_reward
MAX_REASONABLE_SCORE = GRID_COUNT * GRID_COUNT * POINTS_PER_FOOD


def coins_for_score(score, reward):
    """500 -> 1x reward, 1000 -> 2x, ... (below 500 earns nothing)."""
    return (score // SCORE_STEP) * reward


@snake_bp.route("/8-bit/games/snake")
@login_required
def snake():
    uid = session["user_id"]
    return render_template("snake.html", coins=get_coins(uid),
                       high_score=get_high_score(uid, GAME_NAME),
                       plays_left=plays_left(uid, GAME_NAME),
                       max_lives=PLAYS_PER_GAME_PER_DAY,
                       points_per_food=POINTS_PER_FOOD,
                       score_step=SCORE_STEP,
                       coin_reward=get_game(GAME_NAME).coin_reward)

@snake_bp.route("/8-bit/games/snake/api/finish", methods=["POST"])
@login_required
def finish_run():
    """The browser plays the game and reports the final score; the server
    decides coins and high score."""
    uid = session["user_id"]
    data = request.get_json(silent=True) or {}
    score = data.get("score")

    if (
        type(score) is not int          # rejects bools, floats, strings
        or score < 0
        or score > MAX_REASONABLE_SCORE
        or score % POINTS_PER_FOOD != 0  # scores only come in multiples of a food
    ):
        return jsonify({"error": "invalid score"}), 400

    if plays_left(uid, GAME_NAME) == 0:
        return jsonify({"error": "no plays left today"}), 403

    previous_best = get_high_score(uid, GAME_NAME)  # read BEFORE recording this run
    awarded = coins_for_score(score, get_game(GAME_NAME).coin_reward)

    coins = record_play(uid, GAME_NAME, score=score, coins_earned=awarded)
    if coins is None:
        return jsonify({"error": "no plays left today"}), 403

    return jsonify({
        "awarded": awarded,
        "coins": coins,
        "high_score": max(previous_best, score),
        "new_high_score": score > previous_best,
        "plays_left": plays_left(uid, GAME_NAME),
    })