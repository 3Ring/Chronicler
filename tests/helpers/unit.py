from project.setup.db_init_create.base_items import Base_items
from project.setup import defaults as d
from project.extensions.sql_alchemy import db
from project.helpers.db_session import db_session
from project.models import (
    Users,
    Images,
    Games,
    Characters,
    Sessions,
    Notes,
    Places,
    NPCs,
    Items,
    BridgeUserImages,
    BridgeUserGames,
    BridgeGameCharacters,
    BridgeGamePlaces,
    BridgeGameNPCs,
    BridgeGameItems,
)

models = [
    Users,
    Images,
    Games,
    Characters,
    Sessions,
    Notes,
    Places,
    NPCs,
    Items,
    BridgeUserImages,
    BridgeUserGames,
    BridgeGameCharacters,
    BridgeGamePlaces,
    BridgeGameNPCs,
    BridgeGameItems,
]


def build(app):
    """
    This function initializes the database with the admin and orphanage rows

    :param app: The Flask app object
    """
    Base_items.init_database_assets(app)
    admins = [
        Users,
        Characters,
        Games,
    ]
    for a in admins:
        assert a.query.get(d.Admin.id) is not None
    for m in models:
        assert m.query.get(d.Orphanage.id) is not None


def _reset_empty():
    """
    Reset the database to an empty state
    """
    with db_session():
        for m in models:
            db.session.query(m).delete()
    for m in models:
        assert len(m.query.all()) == 0

