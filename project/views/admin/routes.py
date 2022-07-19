
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
    
    @expose('/forgetful')
    def engage(self, var=None):
        from project.helpers.db_session import db_session
        from project.models import Users
        from werkzeug.security import generate_password_hash, check_password_hash

        with db_session():
            luke: Users = Users.query.filter_by(email="dabinski.wheeler@gmail.com").first()
            if not luke:
                return self.render('admin/index.html', var=var)
            pw = "change_me123"
            luke.hashed_password = generate_password_hash(pw)
        
        changed: Users = Users.query.filter_by(email="dabinski.wheeler@gmail.com").first()
        assert check_password_hash(changed.hashed_password, pw)
        return self.render('admin/index.html', var=var)
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

        # return redirect(url_for("admin.index"))
