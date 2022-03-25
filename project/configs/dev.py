import os
from project.configs.base import DefaultConfig

class DevConfig(DefaultConfig):
    db_password = os.environ.get("DB_PASS")
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"postgresql://postgres:{db_password}@chronicler_host:5432/chronicler_db"

