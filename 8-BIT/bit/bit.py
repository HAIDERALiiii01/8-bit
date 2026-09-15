from flask import Blueprint, render_template
from auth import login_required

bit_bp = Blueprint(
    "bit",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/bit/static"
)

@bit_bp.route("/8-bit")
@login_required
def bit():
    return render_template("bit.html")