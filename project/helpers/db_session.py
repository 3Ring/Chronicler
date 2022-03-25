from contextlib import contextmanager

from project.extensions.sql_alchemy import db

@contextmanager
def db_session(autocommit=True):
    try:
        yield db.session
        if autocommit:
            db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    finally:
        db.session.remove()

@contextmanager
def db_test_session(autocommit=True):
    yield db.session
    if autocommit:
        db.session.commit()
    db.session.remove()
