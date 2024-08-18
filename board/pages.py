from flask import Blueprint, render_template


bp = Blueprint("pages", __name__)

@bp.route("/")
def home()->str:
    """
    redirects to the main page
    """
    return render_template("pages/home.html")

@bp.route("/about")
def about()->str:
    """
    redirects to the about page
    """
    return render_template("pages/about.html")
