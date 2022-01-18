from flask import Blueprint, request
from flask_login import login_required

from project.views.main.index import index_get, index_post

main = Blueprint("main", __name__)


@main.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "GET":
        return index_get()
    return index_post()

