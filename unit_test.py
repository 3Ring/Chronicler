
from project.app import create_app

from project.configs.testing import UnitTestConfig


test = create_app(config=UnitTestConfig)