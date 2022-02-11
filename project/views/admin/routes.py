
from flask_admin import AdminIndexView, expose
from flask import redirect, url_for, Blueprint, flash
from flask_login import current_user

admin_ = Blueprint("admin_", __name__)

from project.setup_ import defaults as d

class AdminIndex(AdminIndexView):
    @expose('/')
    def index(self, var=None):
        if current_user.is_anonymous:
            return redirect(url_for("index.page"))
        if current_user.id != d.Admin.id:
            return redirect(url_for("index.page"))

        
        return self.render('admin/index.html', var=var)
    
@admin_.route("/admin/engage", methods=["GET"])
def engage():
    from project.helpers.db_session import db_session
    from project.models import Users, Characters, Games
    with db_session():
        
        for user in Users.query.all():
            avatar = Characters.create(name=user.name, user_id=user.id, avatar=True)
            avatar.add_to_game(Games.get_bugs().id)
            flash(avatar)

        return redirect(url_for("admin.index"))
