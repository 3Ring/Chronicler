from __future__ import annotations
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from testing.end_to_end.models import Users, DMs, Characters
    from testing.end_to_end.mock import Mock

from dataclasses import dataclass, field

from testing import globals as env

@dataclass
class Games:
    id: int = field(default=None, init=False)
    dm: DMs = None
    name: str = None
    publish: bool = True
    image_path: str = None
    url: str = None
    players: List[Users] = field(default_factory=list)
    characters: List[Characters] = field(default_factory=list)

    def __post_init__(self):
        self.id = next(env.ITERATOR)
        if self.name is None:
            self.name = self.default_name(self.id)
        if self.dm:
            self.dm.game = self

    @staticmethod
    def default_name(id: int):
        return f"GAME {id}"

    def delete(self, mock: Mock, fail=False):
        pass