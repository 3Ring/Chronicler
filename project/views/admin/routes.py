
from flask_admin import AdminIndexView, expose
from flask import redirect, url_for, Blueprint, flash
from flask_login import current_user



admin_ = Blueprint("admin_", __name__)

from project.setup import defaults as d

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
    from project.models import Users, Characters, Games, Notes
    from project.models import BridgeGameCharacters
    with db_session():
        
        # for user in Users.query.all():
        #     # for c in Characters.query.filter_by(user_id=user.id).all():
        #     #     if c.avatar == True:
        #     #         for n in Notes.query.filter_by(origin_character_id=c.id).all():
        #     #             flash(n.origin_character_id)
        #     #             n.delete_self()
        #     #         for br in BridgeGameCharacters.query.filter_by(character_id=c.id).all():

        #     #             flash(br.game_id)
        #     #             br.delete_self()
        #     #         flash(c.name)
        #     #         c.delete_self()
        #     if user.id > 0:
        #         avatar = Characters.create(name=user.name, user_id=user.id, avatar=True)
        #         avatar.add_to_game(Games.get_bugs().id)
        #         flash(avatar.name)

        return redirect(url_for("admin.index"))
