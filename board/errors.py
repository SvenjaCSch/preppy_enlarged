from flask import current_app, render_template, request
from typing import Any

def page_not_found(e:Any)->Any:
    """
    provides page not found error
    """
    current_app.logger.info(f"'{e.name}' error ({e.code}) at {request.url}")
    return render_template("errors/404.html"), 404