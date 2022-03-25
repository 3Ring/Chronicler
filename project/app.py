import os
from flask import Flask
from project.setup.config import config_app as config_app
from project.setup.helpers import prep_db
from project.setup.blueprints import init_blueprints
from project.setup.extensions import configure_extensions


def create_app(config=None, create=False, testing=False):
    """Create and configure an instance of the Flask application."""

    from dotenv import load_dotenv
    # print(f'os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"): {os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")}')
    load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))
    # print(f'os.path.dirname(__file__): {os.path.dirname(__file__)}')
    try:
        app = Flask(__name__)
        # print(f'app.root_path: {app.root_path}')
        # print(f'app.instance_path: {app.instance_path}')
        # app.app_context()
        # if not os.path.exists(app.instance_path):
        #     os.makedirs(app.instance_path)
        # app.test_request_context
        # app.test_client
        config_app(app, config)
        configure_extensions(app)
        if not app.testing:
            prep_db(app, create, __file__, testing)
        init_blueprints(app)
        return app
    except Exception as e:
        print(f"create_app Exception is: {e} type is: {type(e)}")
        raise e
