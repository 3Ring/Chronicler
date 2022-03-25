from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils.functions import database_exists
db = SQLAlchemy()

# def prep_db(app):
#     if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
#         print("No database found..", "\ncreating database...")
#         from project.setup.helpers import create_db
#         create_db(app)
#     with app.app_context():
#         upgrade()
#     from project.setup.db_init_create.base_items import Base_items
#     Base_items.init_database_assets(app)

