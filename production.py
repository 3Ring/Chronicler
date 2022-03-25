from project.app import create_app
from project.configs.base import DefaultConfig


dev = create_app(config=DefaultConfig)
