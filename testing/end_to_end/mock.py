from __future__ import annotations

from collections import deque
from typing import Callable, Deque
from dataclasses import dataclass, field
from contextlib import contextmanager
import logging

from testing.end_to_end.browser import BrowserUI
from testing.end_to_end.models import Users
from testing import ExpectedException
from testing.globals import LOGGER


@dataclass
class Mock:
    ui: BrowserUI
    user: Users
    extra_users: Deque[Users] = field(default_factory=deque)

    def test_reset(self):
        self.user.delete_attached(self)
        for user in self.extra_users:
            user.delete_attached(self)
            del user
        self.extra_users.clear()
        self.user = Users()
        self.clean_session()

    def clean_session(self):
        LOGGER.debug(f"new user information: {self.user}")
        self.ui.browser.delete_all_cookies()
        self.ui.browser.refresh()

    def add_user(
        self,
        user: Users = None,
        rotate: bool = True,
    ):
        """creates new user to self.user.
        saves appends previous user to self.extra_users
        """
        if user is None:
            user = Users()
        self.extra_users.appendleft(user)
        if rotate:
            self.rotate_user()

    def rotate_user(self):
        """appends current user to the end of the deque
        and places front of deque in self.user"""
        self.extra_users.append(self.user)
        self.user = self.extra_users.popleft()
        self.clean_session()


    @contextmanager
    def test_manager(self, func: Callable):
        try:
            LOGGER.info(f"[[{func.__name__}]]: starting ")
            yield
        except ExpectedException:
            msg = f"[[{func.__name__}]]: failed successfully."
            LOGGER.info(msg + "\n" + ("=" * (len(msg) + 15)))
        except Exception:
            LOGGER.set_create_dump(logging.ERROR)
            LOGGER.console.error(f"[[{func.__name__}]] failed. See logs for details")
            LOGGER.screencap(self.ui.browser, func.__name__, self.ui.browser.name)
            LOGGER.file.error(
                f"\n-Failing test: {func.__name__}\n"
                + f"-browser type: {self.ui.browser.name}\n"
                + f"-mock.user: {self.user}\n"
                + f"-current_url: {self.ui.browser.current_url}",
                exc_info=True,
            )
            raise
        else:
            msg = f"[[{func.__name__}]]: passed successfully."
            LOGGER.info(msg + "\n" + ("=" * (len(msg) + 15)))
        finally:
            self.test_reset()
