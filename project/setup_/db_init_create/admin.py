class CreateAdmins:
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
        )

    @classmethod
    def fill_bugs(cls):
        from project.helpers import bugs_texts
        from project.models import Sessions, Notes

        for s in bugs_texts.bug_sessions():
            Sessions.create(number=s["number"], title=s["title"], game_id=s["game_id"])
        for n in bugs_texts.bug_notes():
            Notes.create(
                charname=n["charname"],
                text=n["text"],
                session_number=n["session_number"],
                user_id=n["user_id"],
                origin_character_id=n["origin_character_id"],
                game_id=n["game_id"],
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
