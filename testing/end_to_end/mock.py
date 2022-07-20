from __future__ import annotations


from dataclasses import dataclass, field
from typing import Callable
from contextlib import contextmanager
import logging



from end_to_end.browser.checks import CheckActions
from end_to_end.browser.ui import BrowserUI
from end_to_end.models.users import Users
import env

from _logging import Logger


@dataclass
class Mock:
    ui: BrowserUI
    logger: Logger
    user: Users
    check: CheckActions
    extra_users: list[Users] = field(default_factory=list)

    def reset(self):
        self.user.reset()
        self.extra_users.clear()
        self.logger.debug(f"new user information: {self.user}")
        self.ui.browser.delete_all_cookies()
        self.ui.browser.refresh()

    def add_user(
        self,
        name: str = None,
        email: str = None,
        password: str = None,
        different_confirm: str = None,
    ):
        """creates new user to self.user.
        saves appends previous user to self.extra_users
        """
        saved = Users(
            self.user.name,
            self.user.email,
            self.user.password,
            self.user.different_confirm,
        )
        self.extra_users.append(saved)
        self.user.new(name, email, password, different_confirm)

    @contextmanager
    def test_manager(self, func: Callable):
        try:
            self.logger.info(f"[[{func.__name__}]]: starting ")
            yield
        except Exception:
            self.logger.set_create_dump(logging.ERROR)
            self.logger.console.error(
                f"[[{func.__name__}]] failed. See logs for details"
            )
            self.logger.screencap(self.ui.browser, func.__name__, self.ui.browser.name)
            self.logger.file.error(
                f"\n-Failing test: {func.__name__}\n"
                + f"-browser type: {self.ui.browser.name}\n"
                + f"-mock.user: {self.user}\n"
                + f"-current_url: {self.ui.browser.current_url}",
                exc_info=True,
            )
            raise
        else:
            msg = f"[[{func.__name__}]]: passed successfully."
            self.logger.info(msg + "\n" + ("=" * (len(msg) + 15)))
        finally:
            self.reset()
