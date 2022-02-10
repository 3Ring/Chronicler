import os
import flask_migrate


def update_db(app, test_config):
    """Sets up db with Flask Migrate"""

    if test_config is not None:
        app.config.update(test_config)
        return
    flask_migrate.upgrade()
    # flag = ""
    # while flag != "done":
    #     if flag == "":
    #         with app.app_context():
    #             from project.models import Users
    #             admin = Users.query.with_entities(Users.id).filter_by(id=-1).first()
    #             flag = "admin" if admin is not None else "upgrade"

    #     if flag == "admin":
    #         with app.app_context():
    #             flask_migrate.upgrade()
    #             flag = "done"

    #     if flag == "upgrade":
    #         with app.app_context():
    #             flask_migrate.upgrade(revision="51c3bfee43e4")
    #             flag = "delete"

    #     if flag == "delete":
    #         import os
    #         from project.helpers.db_session import db_session
    #         from project.models import (
    #             Users,
    #             BridgeUserGames,
    #             BridgeUserImages,
    #             NPCs,
    #             Notes,
    #             Characters,
    #         )
    #         with app.app_context():
    #             with db_session(autocommit=False) as sess:
    #                 _admin = Users.query.filter_by(email=os.environ.get("ADMIN_EMAIL")).first()
    #                 to_delete = []
    #                 to_delete.append(BridgeUserGames.query.filter_by(user_id=_admin.id).all())
    #                 to_delete.append(BridgeUserImages.query.filter_by(user_id=_admin.id).all())
    #                 to_delete.append(NPCs.query.filter_by(user_id=_admin.id).all())
    #                 to_delete.append(Notes.query.filter_by(user_id=_admin.id).all())
    #                 to_delete.append(Characters.query.filter_by(user_id=_admin.id).all())
    #                 to_delete.append([_admin])
    #                 for to_del in to_delete:
    #                     if to_del is not None:
    #                         for to in to_del:
    #                             to.delete_self()
    #                     sess.commit()
    #         flag = "next"

    #     if flag == "next":
    #         transfer_game_id(app)
    #         flag = "init"

    #     if flag == "init":
    #         from project.setup_.db_init_create.base_items import Base_items
    #         Base_items.init_database_assets(app)
    #         update_data(app)
    #         flag = "admin"



def transfer_game_id(app):
    from project.helpers.db_session import db_session
    from project.models import Characters, BridgeGameCharacters
    with app.app_context():
        with db_session(autocommit=False) as sess:
            for c in Characters.query.all():
                brs = BridgeGameCharacters.query.filter_by(character_id=c.id).all()
                if c not in brs:
                    BridgeGameCharacters.create(character_id=c.id, game_id=c.game_id)
                c.game_id = None
            sess.commit()

def update_data(app):
    from project.helpers.db_session import db_session
    from project.models import (
        Users,
        Notes,
        Characters,
        Games,
        Images,
    )
    from project.views.edit.game_dm import delete_game_and_assets

    with app.app_context():
        with db_session(autocommit=False) as sess:
            # add charname to notes
            for n in Notes.query.all():
                if getattr(n, "charname", None) is None:
                    try:
                        name = Characters.query.get(n.origin_character_id).name
                    except KeyError:
                        name = Characters.query.get(n.character).name
                    finally:
                        n.charname = name
            sess.commit()

            # adjust dm avatar
            for c in Characters.query.all():
                if c.name == "DM":
                    c.dm = True
            sess.commit()
            # create and place user avatars
            for user in Users.query.all():
                if user.id > 0:
                    avatar = Characters.create(
                        name=user.name, user_id=user.id, avatar=True
                    )
                    avatar.add_to_game(Games.get_bugs().id)
            sess.commit()
            # correct img strings
            for i in Images.query.all():
                if (
                    i.img_string[: len("data:image/jpeg;base64,")]
                    != "data:image/jpeg;base64,"
                ):
                    i.img_string = "data:image/jpeg;base64," + i.img_string
            sess.commit()
            # delete unused games
            for g in Games.query.all():
                if g.id > 0 and len(Games.get_player_list_from_id(g.id)) < 1:
                    delete_game_and_assets(g)
            sess.commit()


def create_db():
    import psycopg2
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

    db_password = os.environ.get("DB_PASS")
    con = psycopg2.connect(
        f"host='chronicler_host' user='postgres' password='{db_password}'"
    )
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cursor = con.cursor()
    name_Database = "chronicler_db"

    cursor.execute(f"DROP DATABASE IF EXISTS {name_Database};")
    sqlCreateDatabase = "create database " + name_Database + ";"
    cursor.execute(sqlCreateDatabase)
    print(f"{name_Database} created")
    return


def postfix(string):
    if string is None:
        return None
    else:
        if string[0:9] == "postgres:":
            new = "postgresql" + string[8:]
            return new
        else:
            return string
