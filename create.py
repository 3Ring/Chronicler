from project.app import create_app
from project.configs.dev import DevConfig


install = create_app(config=DevConfig, create=True)