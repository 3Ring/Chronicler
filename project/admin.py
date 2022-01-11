from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose
from flask import redirect, url_for
from flask_login import current_user
from project import defaults as d

class AdminIndex(AdminIndexView):
    @expose('/')
    def index(self):
        if current_user.is_anonymous:
            return redirect(url_for("main.index"))
        if current_user.id != d.Admin.id:
            return redirect(url_for("main.index"))
        var = "test"
        return self.render('admin/index.html', var=var)

def init_admin(admin, db):
    from project import models
    
    admin.add_view(ModelView(models.Users, db.session, category="Main"))
    admin.add_view(ModelView(models.Images, db.session, category="Main"))
    admin.add_view(ModelView(models.Games, db.session, category="Main"))
    admin.add_view(ModelView(models.Characters, db.session, category="Main"))
    admin.add_view(ModelView(models.Sessions, db.session, category="Main"))
    admin.add_view(ModelView(models.Notes, db.session, endpoint="Notes_", category="Main"))
    admin.add_view(ModelView(models.Places, db.session, category="Main"))
    admin.add_view(ModelView(models.NPCs, db.session, category="Main"))
    admin.add_view(ModelView(models.Items, db.session, category="Main"))
    admin.add_view(ModelView(models.BridgeUserImages, db.session, category="Bridge"))
    admin.add_view(ModelView(models.BridgeUserGames, db.session, category="Bridge"))
    admin.add_view(ModelView(models.BridgeGameCharacters, db.session, category="Bridge"))
    admin.add_view(ModelView(models.BridgeGamePlaces, db.session, category="Bridge"))
    admin.add_view(ModelView(models.BridgeGameNPCs, db.session, category="Bridge"))
    admin.add_view(ModelView(models.BridgeGameItems, db.session, category="Bridge"))


