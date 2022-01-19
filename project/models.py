import base64
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy import orm, text, event
from flask import request
from flask_login import current_user

# from project.form_validators import Character

from project.__init__ import db
from project.setup_ import defaults as d


#######################################
###           Base classes         ####
#######################################

# class ViewsMixin:
#     pass
    # @staticmethod
    # def failure(url, message=None, **kwarg):
    #     """redirects user to url and flashes message"""
    #     if message:
    #         flash(message)
    #     if kwarg:
    #         return redirect(url_for(url, **kwarg))
    #     return redirect(url_for(url))

    # @staticmethod
    # def success(url, message=None, **kwarg):
    #     """redirects user to url and flashes message"""
    #     if message:
    #         flash(message)
    #     if kwarg:
    #         return redirect(url_for(url, **kwarg))
    #     return redirect(url_for(url))


class SAWithImageMixin:
    def attach_image(self):

        self.image_object = Images.query.get(self.img_id)
        if self.image_object:
            self.image = self.image_object.img_string
        return


class SAAdmin:
    @classmethod
    def get_admin(cls):
        return cls.query.filter_by(id=d.Admin.id).first()


class SABaseMixin:

    id = db.Column(db.Integer, primary_key=True)
    removed = db.Column(
        db.Boolean, default=d.Base.removed, server_default=text(d.Base.server_removed)
    )

    # @classmethod
    # def get_from_id(cls, id_: int):
    #     return cls.query.filter_by(id=id_).first()


    @classmethod
    def create(cls, **kw):
        """adds new item to database

        this is inherited by all Chronicler SQLAlchemy classes
        and can be used to also populate join tables
        """
        obj = cls(**kw)
        db.session.add(obj)
        return obj

    @classmethod
    def get_orphanage(cls):
        """Returns orphan class object"""
        return cls.query.get(d.Orphanage.id)

    # def remove_self(self):
    #     self.removed = True
    #     db.session.commit()
    #     return True

    # def unremove_self(self):
    #     self.removed = False
    #     db.session.commit()
    #     return True

    # def edit(self, **kw):
    #     for key, value in kw.items():
    #         # if str(f"{self.__table__}.{key}") in str(self.__table__.columns):
    #         self.key = value
    #         db.session.commit()

    # def _remove_attached(self, dependencies: list = []):
    #     for list_ in dependencies:
    #         for item in list_:
    #             item.remove_self()
    #     return

    # def _delete_attached(self, dependencies: list = [], confirm: bool = False):
    #     """deletes all attached items

    #     :param dependencies: list containing lists of dependencies
    #     :param confirm: confirmation to make sure this wasn't
    #                     used on accident when "remove_self" method was intended
    #     """
    #     if confirm:
    #         for list_ in dependencies:
    #             for item in list_:
    #                 item.delete_self(confirm=confirm)
    #     return

    # def _delete_list(self, item_list: list, confirm: bool = False):
    #     """deletes all items in argument list

    #     :param item_list: list of SQLAlchemy objects to delete
    #     :param confirm: confirmation to make sure this wasn't
    #                     used on accident when "remove_self" method was intended
    #     """
    #     if confirm:

    #     return

    def delete_self(self):
        """deletes SQLAlchemy model from database."""
        db.session.query(self.__class__).filter_by(id=self.id).delete()

    # def _get_new_id(self):
    #     """returns new unused primary key"""
    #     new = self.__class__.query.order_by(self.__class__.id.desc()).first().id
    #     return new + 1

    # def _move_dependencies(self, new_id):
    #     """this is here as a base case. and will be handled at the class level"""
    #     return

    # def _copy_to_new_id(self, new_id, **kw):
    #     """make placeholder in db for moving primary keys"""
    #     self.__class__.create(id=new_id, **kw)

    # def move_self(self, **kw):
    #     """changes primary_key and triggers foreign key changes to dependencies"""
    #     new_id = self._get_new_id()
    #     self._copy_to_new_id(new_id, **kw)
    #     self._move_dependencies(new_id, self.id)
    #     db.session.query(self.__class__).filter_by(id=self.id).delete()
    #     db.session.commit()
    #     return

    def __repr__(self) -> str:
        repr_ = f"{self.__tablename__}("
        for column in self.__table__.columns:
            repr_ += f"{column.key}={getattr(self, str(column.key))}, "
        repr_ = repr_[:-2] + ")"

        return repr_


#######################################
###           Main tables          ####
#######################################


class Users(SAAdmin, SABaseMixin, UserMixin, db.Model):

    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    hashed_password = db.Column(db.String(120), nullable=False)
    date_added = db.Column(db.DateTime, default=d.User.date_added)
    password = None
    # self_title = "user"
    image = d.User.image

    # def _get_pw(self):
    #     return self.password

    # def _set_pw(self, password):
    #     new = generate_password_hash(password, method="sha256")
    #     self.hashed_password = new
    #     self.password = password
    #     # db.session.commit()


    @staticmethod
    def add_to_game(user_id: int, game_id: int) -> object:
        """adds user to join table and returns bridge object"""
        return BridgeUserGames.create(user_id=user_id, game_id=game_id)

    @classmethod
    def get_avatar(cls, user_id):
        for char in Characters.get_list_from_user(user_id, include_avatar=True):
            if char.avatar:
                return char

    @classmethod
    def get_player_list(cls, game_id: int) -> list:
        users = []
        bridge = BridgeUserGames.query.filter_by(game_id=game_id).all()
        for user in bridge:
            users.append(cls.query.get(user.user_id))
        return users

    def get_game_list_player(self):
        player_list = []
        my_games = BridgeUserGames.join(self.id, "user_id", "game_id")
        if my_games:
            for game in my_games:
                if game.dm_id != self.id:
                    player_list.append(Games.query.get(game.id))
        return player_list

    def get_game_list_dm(self):
        return Games.query.filter_by(dm_id=self.id).all()

    # @classmethod
    # def create_simple(cls, **kw):
    #     """adds new User to database and hashes their password.
    #     does not create dependencies
    #     """
    #     kw["hashed_password"] = generate_password_hash(kw["password"], method="sha256")
    #     kw.pop("password")
    #     user = super().create(**kw)
    #     return user

    @classmethod
    def create(cls, **kw):
        """adds new User to database and hashes their password.
        it also adds the user to bug reports
        """
        kw["hashed_password"] = generate_password_hash(kw["password"], method="sha256")
        kw.pop("password")
        user = super().create(**kw)
        return user

    # def remove_self(self):
    #     self._remove_attached()

    # def _remove_attached(self):
    #     dependencies = []
    #     dependencies.append(Games.query.filter_by(dm_id=self.id).all())
    #     dependencies.append(Characters.query.filter_by(user_id=self.id).all())
    #     dependencies.append(Notes.query.filter_by(user_id=self.id).all())
    #     dependencies.append(BridgeUserGames.query.filter_by(user_id=self.id).all())
    #     dependencies.append(BridgeUserImages.query.filter_by(user_id=self.id).all())
    #     super()._remove_attached(dependencies=dependencies)

    def delete_self(self):
        """deletes user from database."""
        self.orphan_attached()
        db.session.delete(self)


    def orphan_attached(self):
        """orphans all attached items"""

        chars = Characters.query.filter_by(user_id=self.id).all()
        for c in chars:
            c.user_id = d.Orphanage.id

        notes = Notes.query.filter_by(user_id=self.id).all()
        for n in notes:
            n.user_id = d.Orphanage.id

        games = Games.query.filter_by(dm_id=self.id).all()
        for g in games:
            g.dm_id = d.Orphanage.id

        npcs = NPCs.query.filter_by(user_id=self.id).all()
        for n in npcs:
            n.user_id = d.Orphanage.id

        bridgeui = BridgeUserImages.query.filter_by(user_id=self.id).all()
        for ui in bridgeui:
            ui.user_id = d.Orphanage.id

        bridgeug = BridgeUserGames.query.filter_by(user_id=self.id).all()
        for ug in bridgeug:
            db.session.delete(ug)


    def get_character_list_from_game(
        self, game_id: int, include_removed: bool = False
    ) -> list:
        """returns a list of all the character objects the user owns in specified game"""
        game_characters = BridgeGameCharacters.join(game_id, "game_id", "character_id")
        final = []
        for c in game_characters:
            if c.user_id == self.id:
                if c.removed:
                    if not include_removed:
                        continue
                final.append(c)
        return final


class Images(SABaseMixin, db.Model):

    img_string = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    self_title = "image"

    @staticmethod
    def _allowed_file(filename):
        ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg"]
        for i, letter in enumerate(filename):
            if letter == "/":
                altered = (filename[i + 1 :]).lower()
                break

        if altered in ALLOWED_EXTENSIONS:
            return True
        return False

    @staticmethod
    def _render_picture(data):

        render_pic = base64.b64encode(data).decode("ascii")
        return render_pic

    @staticmethod
    def _add_decoder(img_string: str, mimetype: str):
        """adds decoder prefix for base 64 image strings"""
        decoder = f"data:{mimetype};base64,"
        return decoder + img_string

    @staticmethod
    def upload(filename) -> int:
        """uploads image data from filename. File name needs to be validated first

        :param filename: file name string ex 'img'
                        this correlates to the 'name' value in the file form input field.
        """
        pic = request.files[filename]
        mimetype = pic.mimetype
        secure_name = secure_filename(pic.filename)
        pic.stream.seek(0)
        data = pic.stream.read()
        render_file = Images._render_picture(data)
        img_string = Images._add_decoder(render_file, mimetype)
        img = Images.create(img_string=img_string, name=secure_name, mimetype=mimetype)
        db.session.flush()
        id_ = img.id
        return id_


class Games(SAAdmin, SABaseMixin, SAWithImageMixin, db.Model):

    name = db.Column(db.String(50), nullable=False)
    published = db.Column(
        db.Boolean,
        default=d.Game.published,
        server_default=text(d.Game.server_published),
        nullable=False,
    )
    date_added = db.Column(db.DateTime, default=d.Game.date_added)
    finished = db.Column(
        db.Boolean, default=d.Game.finished, server_default=text(d.Game.server_finished)
    )

    dm_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    img_id = db.Column(db.Integer, db.ForeignKey("images.id"))
    image_object = object
    image = d.Game.image
    self_title = "game"

    @staticmethod
    def get_index_lists(user) -> dict:
        """Returns a dictionary containing the game lists that the player is in.

        Where dict['player_list'] is a list of Game objects the User is listed as a player in,
        and dict['dm_list'] is a list of Game objects the User is listed in as the 'DM'."""
        game_lists = {}

        game_lists["player_list"] = user.get_game_list_player()

        # game_lists["player_list"]=Games.query.filter(
        #     Games.dm_id != User.id,
        #     Games.id.in_(
        #     BridgeUserGames.query.with_entities(BridgeUserGames.game_id).
        #     filter(BridgeUserGames.user_id.in_(
        #     Users.query.with_entities(
        #     Users.id).filter_by(
        #     id=User.id))))
        # ).all()
        game_lists["dm_list"] = user.get_game_list_dm()
        return game_lists

    @staticmethod
    def get_player_list_from_id(game_id: int) -> list:
        join = BridgeUserGames.join(game_id, "game_id", "user_id")
        game = Games.query.get(game_id)
        for i, user in enumerate(join):
            if user.id == game.dm_id:
                join.pop(i)
                break
        return join

    @classmethod
    def remove_player(cls, user_id: int, game_id: int):
        bridge = BridgeUserGames.query.filter_by(
            user_id=user_id, game_id=game_id
        ).first()
        bridge.delete_self()

    @classmethod
    def remove_character_from_id(cls, character_id):
        bridge = BridgeGameCharacters.query.filter_by(character_id=character_id).first()
        if not bridge:
            return False
        bridge.delete_self()
        return True

    @classmethod
    def get_personal_game_list_dm(cls, user_id: int) -> list:
        """returns a list of all games where user_id == Games.dm_id"""
        return cls.query.filter_by(dm_id=user_id).all()

    @classmethod
    def get_dm_from_gameID(cls, game_id: int):
        """returns user of game"""

        game = cls.query.get(game_id)
        return Users.query.get(game.dm_id)

    @classmethod
    def get_dmID_from_gameID(cls, game_id: int) -> int:
        """returns user_id of game dm"""

        return Games.query.get(game_id).dm_id

    @classmethod
    def get_dm_avatar(cls, game_id: int):
        """returns dm avatar for game"""
        game = cls.query.get(game_id)
        char_list = Characters.get_characters_list_for_game(game.dm_id, game_id)
        for char in char_list:
            if char.dm == True:
                return char
        return False

    @classmethod
    def get_personal_game_list_player(cls, user_id: int) -> list:
        """returns a list of all games the user has a character in"""
        final = []
        bridges = BridgeUserGames.query.filter_by(user_id=user_id).all()
        for bridge in bridges:
            game = Games.query.get(bridge.game_id)
            if game.dm_id != current_user.id:
                final.append(game)
        return final

    @classmethod
    def get_bugs(cls):
        return cls.get_admin()

    @classmethod
    def get_my_joinable(cls):
        published = cls.get_published()
        final_list = []
        for game in published:
            if not BridgeUserGames.query.filter_by(
                user_id=current_user.id, game_id=game.id
            ).all():
                final_list.append(game)
        return final_list

    @classmethod
    def get_published(cls):
        published_list = cls.query.filter(Games.published == True).all()
        final_list = []
        for game in published_list:
            if game.dm_id != current_user.id:
                final_list.append(game)
        return final_list

    @classmethod
    def _fill_bugs(cls):
        tutorial_user = Users.get_admin()
        tutorial_character = Characters.get_admin()
        from project.helpers.bugs_texts import _bug_sessions, _bug_texts

        for session in _bug_sessions:
            Sessions.create(
                number=session["number"],
                title=session["title"],
                game_id=session["game_id"],
            )
        for note in _bug_texts:
            Notes.create(
                charname=tutorial_character.name,
                text=note["text"],
                session_number=note["session_number"],
                private=False,
                to_dm=False,
                user_id=tutorial_user.id,
                origin_character_id=tutorial_character.id,
                game_id=d.Admin.id,
            )

    @classmethod
    def create(cls, **kw):
        """adds new Game to database

        :param name: `String(50), nullable=False)`
        :param published: `Boolean, default=False, nullable=False`
        :param date_added: `DateTime, default=datetime.utcnow`

        :param dm_id: = `Integer, ForeignKey('users.id'), nullable=False`
        :param img_id: = `Integer, ForeignKey('images.id')`
        """
        game = cls(**kw)
        db.session.add(game)

        return game

    def _delete_attached(self, confirm: bool = False):
        """deletes all attached items

        :param confirm: confirmation to make sure this wasn't
                        used on accident when "remove_self" method was intended
        """
        if confirm:
            dependencies = []
            dependencies.append(Notes.query.filter_by(game_id=self.id).all())
            dependencies.append(Sessions.query.filter_by(game_id=self.id).all())
            dependencies.append(BridgeUserGames.query.filter_by(game_id=self.id).all())
            dependencies.append(
                BridgeGameCharacters.query.filter_by(game_id=self.id).all()
            )
            dependencies.append(BridgeGameNPCs.query.filter_by(game_id=self.id).all())
            dependencies.append(BridgeGamePlaces.query.filter_by(game_id=self.id).all())
            dependencies.append(BridgeGameItems.query.filter_by(game_id=self.id).all())

            return super()._delete_attached(dependencies, confirm=confirm)

    def new_game_training_wheels(self):
        """add tutorial notes and session zero to game"""

        tutorial_user = Users.get_admin()

        tutorial_character = Characters.get_admin()
        session = Sessions.create(
            number=0, title="The Adventure Begins!", game_id=self.id
        )
        note_texts = [
            # note 1
            """
            <p><strong class="ql-size-huge"><u>Intro Note 1:</u></strong></p><p>Welcome to your next great adventure!</p><p><br></p><p>This is a place where you can write and share notes.</p>
            """,
            # note 2
            """
            <p><strong class="ql-size-huge"><u>Intro Note 2:</u></strong></p><p>Notes are ordered by "Session" by which we typically mean game session, but for you it can mean whatever you want!</p><p><br></p><p>For your "Session Zero" notes I recommend you have notes related to the overall shape of your game. A short list would be:</p><p><br></p><ol><li>house rules</li><li>areas of roleplay and story that are off limits due to player comfort</li><li>expectations</li></ol><ul><li>how long each session should be</li><li>how often you plan to meet</li><li>what you will do if a player can't make it</li><li>etc!</li></ul>
            """,
            # note 3
            """
            <p><strong class="ql-size-huge"><u>Intro Note 3:</u></strong></p><p>you can edit and delete your notes whenever you like, and though you can't typically delete other player's note, you are more than welcome to get rid of mine if you are already experts!</p>
            """,
            # note 4
            """
            <p><strong class="ql-size-huge"><u>Intro note 4:</u></strong></p><p>Right now this site is in an Alpha phase, which means Chronicler is just a baby!</p><p><br></p><p>If you notice anything that seems broken or could be improved please let me know so I can make it better!</p>
            """,
            # note 5
            """
            <p><strong class="ql-size-huge"><u>Intro Note 5:</u></strong></p><p>This is the last note in the session!</p><p><br></p><p><em>Then why is it at the top?</em></p><p><br></p><p>Chronicler is designed to be a collaborative note taking application. That means that it's meant to be used while you are playing together! We think it's better if the newest notes appear at the top of the page.</p><p><br></p><p>Don't worry, you can change this if you like....<strong>(eventually)</strong></p>
            """,
        ]
        for text in note_texts:
            Notes.create(
                charname=tutorial_character.name,
                text=text,
                session_number=session.number,
                user_id=tutorial_user.id,
                origin_character_id=tutorial_character.id,
                game_id=self.id,
            )

    @orm.reconstructor
    def init_on_load(self):
        self.attach_image()


class Characters(SAAdmin, SABaseMixin, SAWithImageMixin, db.Model):

    name = db.Column(db.String(50), nullable=False)
    bio = db.Column(db.Text)
    avatar = db.Column(
        db.Boolean,
        default=d.Character.avatar,
        server_default=text(d.Character.server_avatar),
    )
    dm = db.Column(
        db.Boolean, default=d.Character.dm, server_default=text(d.Character.server_dm)
    )
    copy = db.Column(
        db.Boolean,
        default=d.Character.copy,
        server_default=text(d.Character.server_copy),
        nullable=False,
    )
    date_added = db.Column(db.DateTime, default=d.Character.date_added)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    # game_id = db.Column(db.Integer, db.ForeignKey('games.id'))
    img_id = db.Column(db.Integer, db.ForeignKey("images.id"))
    img_object = d.Character.img_object
    image = d.Character.image


    def get_my_games(self) -> list:
        """returns a list of all games self is attached to"""
        return BridgeGameCharacters.join(self.id, "character_id", "game_id")

    def add_to_game(self, game_id: int):
        bridge = BridgeGameCharacters.query.filter_by(
            character_id=self.id, game_id=game_id
        ).first()
        if bridge:
                raise BaseException("character already in game")
        BridgeGameCharacters.create(character_id=self.id, game_id=game_id)


    def _delete_attached(self, confirm: bool = False):
        """deletes all attached items

        :param confirm: confirmation to make sure this wasn't
                        used on accident when "remove_self" method was intended
        """
        if confirm:
            dependencies = []
            dependencies.append(
                Notes.query.filter_by(origin_character_id=self.id).all()
            )
            dependencies.append(
                BridgeGameCharacters.query.filter_by(character_id=self.id).all()
            )
            # dependencies.append(
            return super()._delete_attached(dependencies, confirm=confirm)

    @staticmethod
    def get_player_character_list_for_game(
        game_id: int, include_removed: bool = False
    ) -> list:
        """returns a list of all the character objects the user owns in specified game"""
        game_characters = BridgeGameCharacters.join(game_id, "game_id", "character_id")
        final = []
        for c in game_characters:
            if c.user_id == current_user.id:
                if c.removed:
                    if not include_removed:
                        continue
                final.append(c)
        return final

    @classmethod
    def add_character_to_game(cls, character_id: int, game_id: int):
        adding = cls.query.get(character_id)
        if adding:
            if adding.add_to_game(game_id):
                return True
        return False

    @classmethod
    def get_list_from_user(
        cls,
        user_id: int,
        include_avatar: bool = False,
        include_dm: bool = False,
        include_removed: bool = False,
    ) -> list:
        """Returns a list of all characters attached to the provided user_id.

        does not include characters in bug reports or orphanage

        :param user_id: id of user.
        :param include_avatar: if set to `True` user avatar will be included in the list.
        :param include_dm: if set to `True` dm avatars will be inluded in the list.
        :param include_removed: if set to `True` removed characters will be included.
        """

        my_characters = cls.query.filter_by(user_id=user_id).order_by(cls.name).all()
        if include_avatar:
            pass
        else:
            for i, a in enumerate(my_characters):
                if a.avatar:
                    my_characters.pop(i)
                    break
        if include_removed:
            pass
        else:
            without_removed = []
            for r in my_characters:
                if not r.removed:
                    without_removed.append(r)
            my_characters = without_removed
        if include_dm:
            pass
        else:
            without_dm = []
            for c in my_characters:
                if not c.dm:
                    without_dm.append(c)
            my_characters = without_dm
        return my_characters

    @classmethod
    def get_dm_characters(cls, user_id: int) -> list:

        return

    @classmethod
    def create(cls, follow_up=False, **kw):
        """adds new Character to database

        :param id: `Integer, primary_key=True`
        :param removed: `Boolean default=False`
                    Set to true when character is removed by user.
        :param name: `String(50), nullable=False`
        :param bio: `Text` not implimented for now
        :param dm: `Boolean, default=False`
                 Set to true if character is dm avatar
        :param date_added: `DateTime, default=datetime.utcnow`

        :param user_id: `Integer, db.ForeignKey('users.id'), nullable=False`
        :param img_id: = `Integer, ForeignKey('images.id')`
        """
        obj = super().create(**kw)

        return obj

    @orm.reconstructor
    def init_on_load(self):
        """this is for the character select logic"""
        self.is_npc = False
        self.attach_image()


class Sessions(SABaseMixin, db.Model):

    number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    synopsis = db.Column(db.Text)
    date_added = db.Column(db.DateTime, default=d.Session.date_added)

    game_id = db.Column(db.Integer, db.ForeignKey("games.id"), nullable=False)

    @classmethod
    def get_list_from_gameID(cls, game_id: int) -> list:
        """returns list of sessions in order of Sessions.number"""

        session_list = (
            Sessions.query.filter_by(game_id=game_id).order_by(Sessions.number).all()
        )
        return session_list


class Notes(SABaseMixin, db.Model):

    charname = db.Column(db.String(50), nullable=False)
    text = db.Column(db.Text)
    session_number = db.Column(db.Integer)
    private = db.Column(db.Boolean)
    to_dm = db.Column(db.Boolean)
    date_added = db.Column(db.DateTime, default=d.Note.date_added)
    char_img = d.Note.char_img

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    origin_character_id = db.Column(
        db.Integer, db.ForeignKey("characters.id"), nullable=False
    )

    game_id = db.Column(db.Integer, db.ForeignKey("games.id"), nullable=False)


    @classmethod
    def get_list_from_session_number(cls, session_number, game_id):
        return (
            cls.query.filter_by(game_id=game_id)
            .filter_by(session_number=session_number)
            .order_by(Notes.date_added)
            .all()
        )

    @staticmethod
    def attach_char_img(target):
        character_object = Characters.query.get(target.origin_character_id)
        if character_object:
            img = Images.query.get(character_object.img_id)
            if img:
                target.char_img = img.img_string
            elif character_object.dm:
                target.char_img = d.Images.character_dm


@event.listens_for(Notes, "refresh")
def init_on_refresh(target, args, kwargs):
    """attach image string to instanced class"""
    Notes.attach_char_img(target)


@event.listens_for(Notes, "load")
def init_on_refresh(target, context):
    """attach image string to instanced class"""
    Notes.attach_char_img(target)


class Places(SABaseMixin, db.Model):

    name = db.Column(db.String(40), nullable=False)
    bio = db.Column(db.Text, default=d.Place.bio)
    secret_bio = db.Column(db.Text)
    date_added = db.Column(db.DateTime, default=d.Place.date_added)

    self_title = "place"

    def _delete_attached(self, confirm: bool = False):
        """deletes all attached items

        :param confirm: confirmation to make sure this wasn't
                        used on accident when "remove_self" method was intended
        """
        if confirm:
            dependencies = []
            dependencies.append(
                BridgeGamePlaces.query.filter_by(place_id=self.id).all()
            )
            return super()._delete_attached(dependencies, confirm=confirm)


class NPCs(SAWithImageMixin, SABaseMixin, db.Model):
    __tablename__ = "npcs"

    name = db.Column(db.String(40), nullable=False)
    secret_name = db.Column(db.String(40))
    bio = db.Column(db.Text, default=d.NPC.bio)
    secret_bio = db.Column(db.Text)
    date_added = db.Column(db.DateTime, default=d.NPC.date_added)

    img_id = db.Column(db.Integer, db.ForeignKey("images.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey("places.id"))
    self_title = "NPC"

    def _delete_attached(self, confirm: bool = False):
        """deletes all attached items

        :param confirm: confirmation to make sure this wasn't
                        used on accident when "remove_self" method was intended
        """
        if confirm:
            dependencies = []
            dependencies.append(BridgeGameNPCs.query.filter_by(npc_id=self.id).all())
            return super()._delete_attached(dependencies, confirm=confirm)

    @classmethod
    def get_list(cls, user_id):
        return cls.query.filter_by(user_id=user_id).order_by(cls.name).all()

    @orm.reconstructor
    def init_on_load(self):
        """this is for the character select logic"""
        self.is_npc = True
        self.attach_image()


class Items(SABaseMixin, db.Model):

    name = db.Column(db.String(40), nullable=False)
    bio = db.Column(db.Text, default=d.Item.bio)
    copper_value = db.Column(db.Integer, default=0)
    date_added = db.Column(db.DateTime, default=d.Item.date_added)

    # owner_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    self_title = "loot"

    def _delete_attached(self, confirm: bool = False):
        """deletes all attached items

        :param confirm: confirmation to make sure this wasn't
                        used on accident when "remove_self" method was intended
        """
        if confirm:
            dependencies = []
            dependencies.append(BridgeGameItems.query.filter_by(item_id=self.id).all())
            return super()._delete_attached(dependencies, confirm=confirm)


#######################################
###       Bridge Base classes      ####
#######################################
class BridgeBase:
    @classmethod
    def _get_column_attr(cls, model_id, input_column_name: str):
        return cls.query.filter_by(**{input_column_name: model_id}).all()

    @classmethod
    def join(
        cls,
        model_id,
        input_column_name: str,
        output_column_name: str,
        include_removed: bool = False,
    ) -> list:
        """Uses bridge table and returns all objects from connected table that the model's id is associated with
        will return an incorrect list if not used with correct Bridge Class

        :param model_id: id that you want to use for the search
        :param input_column_name: name of Bridge column associated with the input model
        :param output_column_name: name of Brige column associated with the associated models
        """
        bridge_list = cls._get_column_attr(model_id, input_column_name)
        my_keys = []
        if not bridge_list:
            return False
        for bridge in bridge_list:
            if bridge.removed:
                if not include_removed:
                    continue
            my_keys.append(getattr(bridge, output_column_name))
        model = cls._switch(output_column_name)
        if not model:
            raise BaseException("invalid model in join function")
        my_items = []
        if not my_keys:
            return False
        for key in my_keys:
            item = model.query.get(key)
            if item.removed:
                if not include_removed:
                    continue
            my_items.append(item)
        return my_items

    @classmethod
    def _switch(cls, fkey_name):

        if fkey_name == "user_id":
            return Users
        elif fkey_name == "img_id":
            return Images
        elif fkey_name == "game_id":
            return Games
        elif fkey_name == "character_id":
            return Characters
        elif fkey_name == "place_id":
            return Places
        elif fkey_name == "npc_id":
            return NPCs
        elif fkey_name == "item_id":
            return Items
        return False


#######################################
###       Many-to-many tables      ####
#######################################


class BridgeUserImages(SABaseMixin, BridgeBase, db.Model):
    """multi-relational database joining character item assets"""

    __tablename__ = "bridgeimages"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    img_id = db.Column(db.Integer, db.ForeignKey("images.id"))


class BridgeUserGames(SABaseMixin, BridgeBase, db.Model):
    """multi-relational database joining Users and Games.

    :param owner: `Boolean, default=False` set to true if the user_id is the owner of the game.

    :param user_id: `Integer, ForeignKey('users.id'), nullable=False`
    :param user_id: `Integer, ForeignKey('games.id'), nullable=False`
    """

    __tablename__ = "players"

    owner = db.Column(
        db.Boolean,
        default=d.BridgeUserGame.owner,
        server_default=text(d.BridgeUserGame.server_owner),
    )
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey("games.id"), nullable=False)

    self_title = "player"

    @classmethod
    def create(cls, **kw):
        """adds new BridgeUserGame to database

        :param owner: `Boolean, default=False` set this if the User is dm of game
        :param date_added: `DateTime, default=datetime.utcnow`

        :param user_id: = `Integer, ForeignKey('user.id'), nullable=False`
        :param game_id: = `Integer, ForeignKey('game.id'), nullable=False`
        """
        return super().create(**kw)


class BridgeGameCharacters(SABaseMixin, BridgeBase, db.Model):
    """multi-relational database joining character game assets"""

    __tablename__ = "bridgecharacters"

    game_id = db.Column(db.Integer, db.ForeignKey("games.id"))
    character_id = db.Column(db.Integer, db.ForeignKey("characters.id"))
    dm = db.Column(
        db.Boolean,
        default=d.BridgeCharacter.dm,
        server_default=text(d.BridgeCharacter.server_dm),
    )

    @classmethod
    def create(cls, **kw):
        """adds new BridgeGameCharacter to database

        :param dm: `Boolean` set to `True` if character is dm avatar.

        :param game_id: `Integer, db.ForeignKey("characters.id")`
        :param character: `Integer, db.ForeignKey("games.id")`
        """
        return super().create(**kw)


class BridgeGamePlaces(SABaseMixin, BridgeBase, db.Model):
    """multi-relational database joining Place game assets"""

    __tablename__ = "bridgeplaces"

    game_id = db.Column(db.Integer, db.ForeignKey("games.id"))
    place_id = db.Column(db.Integer, db.ForeignKey("places.id"))


class BridgeGameNPCs(SABaseMixin, BridgeBase, db.Model):
    """multi-relational database joining NPC game assets"""

    __tablename__ = "bridgenpcs"

    game_id = db.Column(db.Integer, db.ForeignKey("games.id"))
    npc_id = db.Column(db.Integer, db.ForeignKey("npcs.id"))


class BridgeGameItems(SABaseMixin, BridgeBase, db.Model):
    """multi-relational database joining character item assets"""

    __tablename__ = "bridgeitems"

    game_id = db.Column(db.Integer, db.ForeignKey("games.id"))
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
