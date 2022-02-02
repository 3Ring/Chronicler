from flask import Blueprint
from flask_login import login_required

from project.views.main.index import index_get

main = Blueprint("main", __name__)


@main.route("/", methods=["GET"])
@login_required
def index():
    return index_get()

