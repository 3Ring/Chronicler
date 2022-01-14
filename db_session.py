from contextlib import contextmanager
from project.__init__ import db

@contextmanager
def db_session(autocommit=True):
    try:
        yield db.session
        if autocommit:
            db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        raise
    finally:
        db.session.remove()
        