import os
from dotenv import load_dotenv
print(f'os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"): {os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")}')
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

from project.app import create_app # noqa
from project import events # noqa

