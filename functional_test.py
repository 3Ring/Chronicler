
from project.app import create_app

from project.configs.testing import FunctionalTestConfig


test = create_app(config=FunctionalTestConfig, create=True, testing=True)