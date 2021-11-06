import os

from project.__init__ import create_app

if os.environ.get("HEROKU_HOSTING"):
    app = create_app()
else:
    app = create_app