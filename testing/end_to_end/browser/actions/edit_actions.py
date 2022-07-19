from dataclasses import dataclass
from selenium.webdriver.common.by import By

from end_to_end.browser.ui import BrowserUI
from end_to_end.browser.actions.check_actions import CheckActions
from _logging import Logger
from end_to_end.assets import User
import env


@dataclass
class EditActions:
    ui: BrowserUI
    logger: Logger
    user: User
    check: CheckActions

    def account_name(self, new: str):
        """navigate to account edit page and change name"""
        self.ui.nav(env.URL_EDIT_ACCOUNT)
        if new is None:
            return
        self.logger.debug(f"changing name to {new}")
        name = self.ui.get_element(
            (By.CSS_SELECTOR, 'input[name="name-name"][type="text"]')
        )
        if not name.is_displayed():
            reveal_name = self.ui.get_element((By.CSS_SELECTOR, 'a[data-edit="name"]'))
            self.ui.click(reveal_name)
        self.ui.input_text(name, new)
        submit = self.ui.get_element(
            (By.CSS_SELECTOR, 'input[type="submit"][name="name-submit"]')
        )
        self.ui.click(submit)
        self.logger.screencap(self.ui.browser, "account_name")

    def account_email(self, new: str):
        """navigate to account edit page and change email"""
        self.ui.nav(env.URL_EDIT_ACCOUNT)
        if new is None:
            return
        email = self.ui.get_element(
            (By.CSS_SELECTOR, 'input[name="email-email"][type="text"]')
        )
        if not email.is_displayed():
            reveal_email = self.ui.get_element(
                (By.CSS_SELECTOR, 'a[data-edit="email"]')
            )
            self.ui.click(reveal_email)
        self.ui.input_text(email, new)
        submit = self.ui.get_element(
            (By.CSS_SELECTOR, 'input[type="submit"][name="email-submit"]')
        )
        self.ui.click(submit)

    def account_password(self, new: str, confirm: str = None):
        """navigate to account edit page and change password"""
        self.ui.nav(env.URL_EDIT_ACCOUNT)
        if new is None:
            return
        if confirm is None:
            confirm = new
        password = self.ui.get_element(
            (By.CSS_SELECTOR, 'input[name="pass-password"][type="password"]')
        )
        if not password.is_displayed():
            reveal_password = self.ui.get_element(
                (By.CSS_SELECTOR, 'a[data-edit="pass"]')
            )
            self.ui.click(reveal_password)
        self.ui.input_text(password, new)
        confirm_ = self.ui.get_element(
            (By.CSS_SELECTOR, 'input[name="pass-confirm"][type="password"]')
        )
        self.ui.input_text(confirm_, confirm)
        submit = self.ui.get_element(
            (By.CSS_SELECTOR, 'input[type="submit"][name="pass-submit"]')
        )
        self.ui.click(submit)

    def account_delete(self, confirm_email: str = None, fail: bool = False):
        """navigate to account delete page and delete"""
        self.ui.nav(env.URL_EDIT_ACCOUNT_DELETE)
        if confirm_email is None:
            confirm_email = self.user.email
        confirm = self.ui.get_element((By.CSS_SELECTOR, 'input[name="confirm"][type="text"]'))
        self.ui.input_text(confirm, confirm_email)
        url = env.URL_EDIT_ACCOUNT_DELETE if fail else env.URL_AUTH_LOGIN
        submit = self.ui.get_element((By.CSS_SELECTOR, 'input[type="submit"]'))
        self.check.submit_and_check(submit, url)

    def account(
        self,
        name: str = None,
        email: str = None,
        password: str = None,
        different_confirm: str = None,
    ):
        self.account_name(name)
        self.account_email(email)
        self.account_password(password, different_confirm)
