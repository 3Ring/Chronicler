from project.app import create_app
from project.configs.dev import DevConfig


dev = create_app(config=DevConfig)

