from project.helpers.db_session import db_session
from project.setup_.db_init_create.admin import CreateAdmins
from project.setup_.db_init_create.orphanage import CreateOrphanage


class Base_items:
    from project import models

    @classmethod
    def init_database_assets(cls, app):
        """create db admins and orphanages"""
        with app.app_context():
            cls.init_admins()
            cls.init_orphanages()

    @classmethod
    def init_admins(cls):
        missing_admins = cls.check_admins()
        if missing_admins:
            for admin in missing_admins:
                with db_session():
                    getattr(CreateAdmins, admin.lower())()
                    if admin.lower() == "games":
                        CreateAdmins.fill_bugs()
                    

    @classmethod
    def init_orphanages(cls):
        missing_orphanages = cls.check_orphanages()
        if missing_orphanages:
            for orphanage in missing_orphanages:
                with db_session():
                    getattr(CreateOrphanage, orphanage.lower())()
                    

    @classmethod
    def check_admins(cls) -> list:
        missing = []
        if not cls.models.Users.get_admin():
            missing.append(cls.models.Users.__name__)
        if not cls.models.Characters.get_admin():
            missing.append(cls.models.Characters.__name__)
        if not cls.models.Games.get_admin():
            missing.append(cls.models.Games.__name__)
        return missing

    @classmethod
    def check_orphanages(cls) -> list:
        missing = []
        if not cls.models.Users.get_orphanage():
            missing.append(cls.models.Users.__name__)
        if not cls.models.Images.get_orphanage():
            missing.append(cls.models.Images.__name__)
        if not cls.models.Games.get_orphanage():
            missing.append(cls.models.Games.__name__)
        if not cls.models.Characters.get_orphanage():
            missing.append(cls.models.Characters.__name__)
        if not cls.models.Sessions.get_orphanage():
            missing.append(cls.models.Sessions.__name__)
        if not cls.models.Notes.get_orphanage():
            missing.append(cls.models.Notes.__name__)
        if not cls.models.Places.get_orphanage():
            missing.append(cls.models.Places.__name__)
        if not cls.models.NPCs.get_orphanage():
            missing.append(cls.models.NPCs.__name__)
        if not cls.models.Items.get_orphanage():
            missing.append(cls.models.Items.__name__)
        if not cls.models.BridgeUserImages.get_orphanage():
            missing.append(cls.models.BridgeUserImages.__name__)
        if not cls.models.BridgeUserGames.get_orphanage():
            missing.append(cls.models.BridgeUserGames.__name__)
        if not cls.models.BridgeGameCharacters.get_orphanage():
            missing.append(cls.models.BridgeGameCharacters.__name__)
        if not cls.models.BridgeGamePlaces.get_orphanage():
            missing.append(cls.models.BridgeGamePlaces.__name__)
        if not cls.models.BridgeGameNPCs.get_orphanage():
            missing.append(cls.models.BridgeGameNPCs.__name__)
        if not cls.models.BridgeGameItems.get_orphanage():
            missing.append(cls.models.BridgeGameItems.__name__)
        return missing
