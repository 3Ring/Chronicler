from flask import Blueprint
from flask_login import login_required

from project.views.index.index import index_get

index = Blueprint("index", __name__)


@index.route("/index", methods=["GET"])
@login_required
def page():
    return index_get()

