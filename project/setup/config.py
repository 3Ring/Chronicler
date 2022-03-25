# import os
from sqlalchemy_utils.functions import database_exists
from project.configs.dev import DevConfig


def config_app(app, config):
    """configure chronicler"""
    if config is None:
        config = DevConfig
    
    # db_password = os.environ.get("DB_PASS")
    app.config.from_object(config)

    # if config:
        # app.config.update(config)
        # uri = app.config["SQLALCHEMY_DATABASE_URI"]
        # print(1.21)
    # else:
        # uri = set_uri(app)
        # print(1.22)
    # if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
    #     print("No database found..", "\ncreating database...")



    # app.config["SQLALCHEMY_DATABASE_URI"] = uri
    # app.config["SECRET_KEY"] = db_password
    # app.config["POSTGRES_PASSWORD"] = db_password
    # app.config["SQLALCHEMY_ECHO"] = False
    # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

# def set_uri(app):
#     # Heroku
#     if os.environ.get("HEROKU_HOSTING"):
#         print("connecting to heroku...")
#         uri = postfix(os.environ.get("DATABASE_URL"))
#     # local
#     elif os.environ.get("DOCKER_FLAG"):
#         print("connecting to local through docker...")
#         uri = f"postgresql://postgres:{db_password}@chronicler_host:5432/chronicler_db"
#         # uri = f"postgresql://nbaiybhjzwkkpy:{db_password}@chronicler_host:5432/chronicler_db"
    
#     else:
#         print("connecting to local...")
#         uri = "sqlite:///litechronicler.db"

#     return uri

# def postfix(string):
#     """replaces depreciated 'postgres:' with 'postgresql'"""
#     if string is None:
#         return None
#     else:
#         if string[0:9] == "postgres:":
#             new = "postgresql" + string[8:]
#             return new
#         else:
#             return string

# def test_env(app, config):
#     app.config.update(config)
#     load_dotenv(".env")