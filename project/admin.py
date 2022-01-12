from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose
from flask import redirect, url_for
from flask_login import current_user
from sqlalchemy import inspect

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

class ChronView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False

def init_admin(admin, db):
    from project import models

    class UsersView(ChronView):
        column_list = [c_attr.key for c_attr in inspect(models.Users).mapper.column_attrs]
    class ImagesView(ChronView):
        column_list = [c_attr.key for c_attr in inspect(models.Images).mapper.column_attrs]
    class GamesView(ChronView):
        column_list = [c_attr.key for c_attr in inspect(models.Games).mapper.column_attrs]
    class CharactersView(ChronView):
        column_list = [c_attr.key for c_attr in inspect(models.Characters).mapper.column_attrs]
    class SessionsView(ChronView):
        column_list = [c_attr.key for c_attr in inspect(models.Sessions).mapper.column_attrs]
    class NotesView(ChronView):
        column_list = [c_attr.key for c_attr in inspect(models.Notes).mapper.column_attrs]
    class PlacesView(ChronView):
        column_list = [c_attr.key for c_attr in inspect(models.Places).mapper.column_attrs]
    class NPCsView(ChronView):
        column_list = [c_attr.key for c_attr in inspect(models.NPCs).mapper.column_attrs]
    class ItemsView(ChronView):
        column_list = [c_attr.key for c_attr in inspect(models.Items).mapper.column_attrs]
    class BridgeUserImagesView(ChronView):
        column_list = [c_attr.key for c_attr in inspect(models.BridgeUserImages).mapper.column_attrs]
    class BridgeUserGamesView(ChronView):
        column_list = [c_attr.key for c_attr in inspect(models.BridgeUserGames).mapper.column_attrs]
    class BridgeGameCharactersView(ChronView):
        column_list = [c_attr.key for c_attr in inspect(models.BridgeGameCharacters).mapper.column_attrs]
    class BridgeGamePlacesView(ChronView):
        column_list = [c_attr.key for c_attr in inspect(models.BridgeGamePlaces).mapper.column_attrs]
    class BridgeGameNPCsView(ChronView):
        column_list = [c_attr.key for c_attr in inspect(models.BridgeGameNPCs).mapper.column_attrs]
    class BridgeGameItemsView(ChronView):
        column_list = [c_attr.key for c_attr in inspect(models.BridgeGameItems).mapper.column_attrs]

    admin.add_view(UsersView(models.Users, db.session, category="Main"))
    admin.add_view(ImagesView(models.Images, db.session, category="Main"))
    admin.add_view(GamesView(models.Games, db.session, category="Main"))
    admin.add_view(CharactersView(models.Characters, db.session, category="Main"))
    admin.add_view(SessionsView(models.Sessions, db.session, category="Main"))
    admin.add_view(NotesView(models.Notes, db.session, endpoint="Notes_", category="Main"))
    admin.add_view(PlacesView(models.Places, db.session, category="Main"))
    admin.add_view(NPCsView(models.NPCs, db.session, category="Main"))
    admin.add_view(ItemsView(models.Items, db.session, category="Main"))
    admin.add_view(BridgeUserImagesView(models.BridgeUserImages, db.session, category="Bridge"))
    admin.add_view(BridgeUserGamesView(models.BridgeUserGames, db.session, category="Bridge"))
    admin.add_view(BridgeGameCharactersView(models.BridgeGameCharacters, db.session, category="Bridge"))
    admin.add_view(BridgeGamePlacesView(models.BridgeGamePlaces, db.session, category="Bridge"))
    admin.add_view(BridgeGameNPCsView(models.BridgeGameNPCs, db.session, category="Bridge"))
    admin.add_view(BridgeGameItemsView(models.BridgeGameItems, db.session, category="Bridge"))



