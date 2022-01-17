from project.helpers.db_session import db_session

class Base_items:
    from project import models
    from project.setup_ import defaults as d
    

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
            cls.create_admins(missing_admins)

    @classmethod
    def init_orphanages(cls):
        missing_orphanages = cls.check_orphanages()
        if missing_orphanages:
            cls.create_orphanages(missing_orphanages)

    @classmethod
    def create_admins(cls, missing):
        for admin in missing:
            with db_session():
                exec(f"cls.CreateAdmins.{admin.lower()}()")

    @classmethod
    def create_orphanages(cls, missing):
        for orphanage in missing:
            with db_session():
                exec(f"cls.CreateOrphanage.{orphanage.lower()}()")

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

    #######################################
    ###         Creation methods       ####
    #######################################

    class CreateAdmins:
        """inner class purely for organization.
        contains all Admin creation methods"""

        from project import models
        from project.setup_ import defaults as d

        @classmethod
        def users(cls):
            """Creates admin User account"""

            cls.models.Users.create(
                id=cls.d.UserAdmin.id,
                removed=cls.d.UserAdmin.removed,
                name=cls.d.UserAdmin.name,
                email=cls.d.UserAdmin.email,
                password=cls.d.UserAdmin.password,
                date_added=cls.d.UserAdmin.date_added,
            )

        @classmethod
        def games(cls):
            """Creates bug report and comment page"""

            cls.models.Games.create(
                id=cls.d.GameBugs.id,
                finished=cls.d.GameBugs.finished,
                removed=cls.d.GameBugs.removed,
                name=cls.d.GameBugs.name,
                published=cls.d.GameBugs.published,
                date_added=cls.d.GameBugs.date_added,
                img_id=cls.d.GameBugs.img_id,
                dm_id=cls.d.GameBugs.dm_id,
                image=cls.d.GameBugs.image,
                image_object=cls.d.GameBugs.image_object,
                with_follow_up=False,
                bug_report=True
            )

        @classmethod
        def characters(cls):
            """Creates tutorial bot"""
            cls.models.Characters.create(
                id=cls.d.CharacterTutorial.id,
                removed=cls.d.CharacterTutorial.removed,
                name=cls.d.CharacterTutorial.name,
                bio=cls.d.CharacterTutorial.bio,
                date_added=cls.d.CharacterTutorial.date_added,
                dm=cls.d.CharacterTutorial.dm,
                avatar=cls.d.CharacterTutorial.avatar,
                copy=cls.d.CharacterTutorial.copy,
                user_id=cls.d.CharacterTutorial.user_id,
                img_id=cls.d.CharacterTutorial.img_id,
                img_object=cls.d.CharacterTutorial.img_object,
                image=cls.d.CharacterTutorial.image,
            )

    class CreateOrphanage:
        """inner class purely for organization.
        contains all orphanage creation methods"""

        from project import models
        from project.setup_ import defaults as d

        @classmethod
        def users(cls):
            """Creates User orphanage.

            this is used as the fkey when a primary key User is removed
            """
            cls.models.Users.create(
                id=cls.d.UserOrphanage.id,
                removed=cls.d.UserOrphanage.removed,
                name=cls.d.UserOrphanage.name,
                email=cls.d.UserOrphanage.email,
                password=cls.d.UserOrphanage.password,
                date_added=cls.d.UserOrphanage.date_added,
            )

        @classmethod
        def images(cls):
            """Creates Image orphanage.

            this is used as the fkey when a primary key Image is removed
            """
            cls.models.Images.create(
                id=cls.d.ImageOrphanage.id,
                removed=cls.d.ImageOrphanage.removed,
                img_string=cls.d.ImageOrphanage.img_string,
                name=cls.d.ImageOrphanage.name,
                mimetype=cls.d.ImageOrphanage.mimetype,
            )

        @classmethod
        def games(cls):
            """Creates Game orphanage.

            this is used as the fkey when a primary key Game is removed
            """
            cls.models.Games.create(
                id=cls.d.GameOrphanage.id,
                finished=cls.d.GameOrphanage.finished,
                removed=cls.d.GameOrphanage.removed,
                name=cls.d.GameOrphanage.name,
                published=cls.d.GameOrphanage.published,
                date_added=cls.d.GameOrphanage.date_added,
                dm_id=cls.d.GameOrphanage.dm_id,
                img_id=cls.d.GameOrphanage.img_id,
            )

        @classmethod
        def characters(cls):
            """Creates Character orphanage.

            this is used as the fkey when a primary key Character is removed
            """
            cls.models.Characters.create(
                id=cls.d.CharacterOrphanage.id,
                removed=cls.d.CharacterOrphanage.removed,
                name=cls.d.CharacterOrphanage.name,
                bio=cls.d.CharacterOrphanage.bio,
                date_added=cls.d.CharacterOrphanage.date_added,
                dm=cls.d.CharacterOrphanage.dm,
                copy=cls.d.CharacterOrphanage.copy,
                user_id=cls.d.CharacterOrphanage.user_id,
                img_id=cls.d.CharacterOrphanage.img_id,
                img_object=cls.d.CharacterOrphanage.img_object,
                image=cls.d.CharacterOrphanage.image,
            )

        @classmethod
        def sessions(cls):
            """Creates Session orphanage.

            this is used as the fkey when a primary key Session is removed
            """
            new = cls.models.Sessions(
                id=cls.d.SessionOrphanage.id,
                removed=cls.d.SessionOrphanage.removed,
                number=cls.d.SessionOrphanage.number,
                title=cls.d.SessionOrphanage.title,
                synopsis=cls.d.SessionOrphanage.synopsis,
                date_added=cls.d.SessionOrphanage.date_added,
                game_id=cls.d.SessionOrphanage.game_id,
            )

        @classmethod
        def notes(cls):
            """Creates Note orphanage.

            this is used as the fkey when a primary key Note is removed
            """
            cls.models.Notes.create(
                id=cls.d.NoteOrphanage.id,
                removed=cls.d.NoteOrphanage.removed,
                charname=cls.d.NoteOrphanage.charname,
                text=cls.d.NoteOrphanage.text,
                session_number=cls.d.NoteOrphanage.session_number,
                private=cls.d.NoteOrphanage.private,
                to_dm=cls.d.NoteOrphanage.to_dm,
                date_added=cls.d.NoteOrphanage.date_added,
                char_img=cls.d.NoteOrphanage.char_img,
                user_id=cls.d.NoteOrphanage.user_id,
                origin_character_id=cls.d.NoteOrphanage.origin_character_id,
                game_id=cls.d.NoteOrphanage.game_id,
            )

        @classmethod
        def places(cls):
            """Creates Place orphanage.

            this is used as the fkey when a primary key Place is removed
            """
            cls.models.Places.create(
                id=cls.d.PlaceOrphanage.id,
                removed=cls.d.PlaceOrphanage.removed,
                name=cls.d.PlaceOrphanage.name,
                bio=cls.d.PlaceOrphanage.bio,
                secret_bio=cls.d.PlaceOrphanage.secret_bio,
                date_added=cls.d.PlaceOrphanage.date_added,
            )

        @classmethod
        def npcs(cls):
            """Creates NPC orphanage.

            this is used as the fkey when a primary key NPC is removed
            """
            cls.models.NPCs.create(
                id=cls.d.NPCOrphanage.id,
                removed=cls.d.NPCOrphanage.removed,
                name=cls.d.NPCOrphanage.name,
                secret_name=cls.d.NPCOrphanage.secret_name,
                bio=cls.d.NPCOrphanage.bio,
                secret_bio=cls.d.NPCOrphanage.secret_bio,
                date_added=cls.d.NPCOrphanage.date_added,
                img_id=cls.d.NPCOrphanage.img_id,
                place_id=cls.d.NPCOrphanage.place_id,
                user_id=cls.d.NPCOrphanage.user_id,
            )

        @classmethod
        def items(cls):
            """Creates Item orphanage.

            this is used as the fkey when a primary key Item is removed
            """
            cls.models.Items.create(
                id=cls.d.ItemOrphanage.id,
                removed=cls.d.ItemOrphanage.removed,
                name=cls.d.ItemOrphanage.name,
                bio=cls.d.ItemOrphanage.bio,
                copper_value=cls.d.ItemOrphanage.copper_value,
                date_added=cls.d.ItemOrphanage.date_added,
            )

        @classmethod
        def bridgeuserimages(cls):
            """Creates BridgeUserImage orphanage.

            this is used as the fkey when a primary key BridgeUserImage is removed
            """
            cls.models.BridgeUserImages.create(
                id=cls.d.BridgeUserImageOrphanage.id,
                removed=cls.d.BridgeUserImageOrphanage.removed,
                user_id=cls.d.BridgeUserImageOrphanage.user_id,
                img_id=cls.d.BridgeUserImageOrphanage.img_id,
            )

        @classmethod
        def bridgeusergames(cls):
            """Creates BridgeUserGame orphanage.

            this is used as the fkey when a primary key BridgeUserGame is removed
            """
            # new = 
            cls.models.BridgeUserGames.create(
                id=cls.d.BridgeUserGameOrphanage.id,
                removed=cls.d.BridgeUserGameOrphanage.removed,
                owner=cls.d.BridgeUserGameOrphanage.owner,
                user_id=cls.d.BridgeUserGameOrphanage.user_id,
                game_id=cls.d.BridgeUserGameOrphanage.game_id,
            )

        @classmethod
        def bridgegamecharacters(cls):
            """Creates BridgeGameCharacter orphanage.

            this is used as the fkey when a primary key BridgeGameCharacter is removed
            """
            cls.models.BridgeGameCharacters.create(
                id=cls.d.BridgeGameCharacterOrphanage.id,
                removed=cls.d.BridgeGameCharacterOrphanage.removed,
                dm=cls.d.BridgeGameCharacterOrphanage.dm,
                character_id=cls.d.BridgeGameCharacterOrphanage.character_id,
                game_id=cls.d.BridgeGameCharacterOrphanage.game_id,
            )

        @classmethod
        def bridgegameplaces(cls):
            """Creates BridgeGamePlace orphanage.

            this is used as the fkey when a primary key BridgeGamePlace is removed
            """
            cls.models.BridgeGamePlaces.create(
                id=cls.d.BridgeGamePlaceOrphanage.id,
                removed=cls.d.BridgeGamePlaceOrphanage.removed,
                place_id=cls.d.BridgeGamePlaceOrphanage.place_id,
                game_id=cls.d.BridgeGamePlaceOrphanage.game_id,
            )

        @classmethod
        def bridgegamenpcs(cls):
            """Creates BridgeGameNPC orphanage.

            this is used as the fkey when a primary key BridgeGameNPC is removed
            """
            cls.models.BridgeGameNPCs.create(
                id=cls.d.BridgeGameNPCOrphanage.id,
                removed=cls.d.BridgeGameNPCOrphanage.removed,
                npc_id=cls.d.BridgeGameNPCOrphanage.npc_id,
                game_id=cls.d.BridgeGameNPCOrphanage.game_id,
            )

        @classmethod
        def bridgegameitems(cls):
            """Creates BridgeGameItem orphanage.

            this is used as the fkey when a primary key BridgeGameItem is removed
            """
            cls.models.BridgeGameItems.create(
                id=cls.d.BridgeGameItemOrphanage.id,
                removed=cls.d.BridgeGameItemOrphanage.removed,
                item_id=cls.d.BridgeGameItemOrphanage.item_id,
                game_id=cls.d.BridgeGameItemOrphanage.game_id,
            )
