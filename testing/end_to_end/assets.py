from __future__ import annotations
from dataclasses import dataclass, field
from typing import Iterator, ClassVar
from itertools import count


@dataclass
class User:
    id: int = field(default=None, init=False)
    name: str = None
    email: str = None
    password: str = None
    different_confirm: str = None
    player_games: list = field(default_factory=list)
    dm_games: list = field(default_factory=list)
    characters: list = field(default_factory=list)
    iterator: ClassVar[Iterator] = count()

    def __post_init__(self):
        self._set_attrs()

    def _set_attrs(self, reset=False):
        self.id = self.iterator.__next__()
        if self.name is None or reset:
            self.name = self.default_name(self.id)
        if self.email is None or reset:
            self.email = self.default_email(self.id)
        if self.password is None or reset:
            self.password = self.default_password(self.id)
        if self.different_confirm is None or reset:
            self.different_confirm = self.password

    def reset(self):
        self._set_attrs(reset=True)

    def new(
        self,
        name: str = None,
        email: str = None,
        password: str = None,
        different_confirm: str = None,
    ):
        self.id = next(self.iterator)
        self.name = self.default_name(self.id) if name is None else name
        self.email = self.default_email(self.id) if email is None else email
        self.password = self.default_password(self.id) if password is None else password
        self.different_confirm = (
            self.password if different_confirm is None else different_confirm
        )

    def change_password(self, new: str) -> None:
        self.password = new
        self.different_confirm = new

    @staticmethod
    def default_name(id: int):
        return f"test{id}"

    @staticmethod
    def default_email(id: int):
        return f"test{id}@test.com"

    @staticmethod
    def default_password(id: int):
        return f"TestPassword{id}"


@dataclass
class DM:
    id: int = field(default=None, init=False)
    user: User
    game: Game = None
    name: str = None
    image_path: str = None

    def __post_init__(self):
        self.id = self.user.iterator.__next__()
        if self.name is None:
            self.name = self.default_name(self.user.name, self.id)
        if self.game:
            self.game.dm = self

    @staticmethod
    def default_name(name: str, id: int):
        return f"DM {name} {id}"


@dataclass
class Game:
    id: int = field(default=None, init=False)
    dm: DM = None
    name: str = None
    publish: bool = True
    image_path: str = None
    players: list[User] = field(default_factory=list)

    def __post_init__(self):
        self.id = self.dm.user.iterator.__next__()
        if self.name is None:
            self.name = self.default_name(self.dm.user.name, self.id)
        if self.dm:
            self.dm.game = self

    @staticmethod
    def default_name(user_name: str, id: int):
        return f"GAME {user_name} {id}"


@dataclass
class Character:
    id: int = field(default=None, init=False)
    player: User
    name: str = None
    bio: str = None
    image_path: str = None
    games: list[Game] = field(default_factory=list)

    def __post_init__(self):
        self.id = self.player.iterator.__next__()
        if self.name is None:
            self.name = self.default_name(self.player.name, self.id)
        if self.bio is None:
            self.bio = self.default_bio(self.player.name, self.id)
        self.player.characters.append(self)

    @staticmethod
    def default_name(name: str, id: int):
        return f"CHARACTER {name} {id}"

    @staticmethod
    def default_bio(name: str, id: int):
        return f"BIO {name} {id}"
