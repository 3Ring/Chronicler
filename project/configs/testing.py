import os
from project.configs.base import DefaultConfig

class UnitTestConfig(DefaultConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

class FunctionalTestConfig(DefaultConfig):
    db_password = os.environ.get("DB_PASS")
    SQLALCHEMY_DATABASE_URI = f"postgresql://postgres:{db_password}@chronicler_host_test:5432/chronicler_db"