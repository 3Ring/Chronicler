from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from end_to_end.models import Users, Games
    from end_to_end.mock import Mock

from dataclasses import dataclass, field

from testing import globals as env

@dataclass
class DMs:
    id: int = field(default=None, init=False)
    user: Users
    game: Games = None
    name: str = None
    image_path: str = None

    def __post_init__(self):
        self.id = next(env.ITERATOR)
        if self.name is None:
            self.name = self.default_name(self.user.name, self.id)
        if self.game:
            self.game.dm = self

    @staticmethod
    def default_name(name: str, id: int):
        return f"DM {name} {id}"

    def delete(self, mock: Mock, fail=False):
        pass