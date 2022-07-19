from dataclasses import dataclass
from selenium.webdriver.common.by import By

from end_to_end.browser.ui import BrowserUI
from end_to_end.browser.actions.check_actions import CheckActions
from _logging import Logger
from end_to_end.assets import User
import env


@dataclass
class AuthActions:
    ui: BrowserUI
    logger: Logger
    user: User
    check: CheckActions

    def register(self, fail: bool = False):
        """
        registers the Mock user.
        :param fail: set to `True` if the registration will fail. Defaults to False
        """
        self.logger.debug(f"registering: {self.user}")
        self.ui.nav(env.URL_AUTH_REGISTER)
        form_name = self.ui.get_element((By.CSS_SELECTOR, "input[name='name']"))
        form_email = self.ui.get_element((By.CSS_SELECTOR, "input[name='email']"))
        form_password = self.ui.get_element((By.CSS_SELECTOR, "input[name='password']"))
        form_confirm = self.ui.get_element((By.CSS_SELECTOR, "input[name='confirm']"))
        
        self.ui.input_text(form_name, self.user.name)
        self.ui.input_text(form_email, self.user.email)
        self.ui.input_text(form_password, self.user.password)
        self.ui.input_text(form_confirm, self.user.different_confirm)

        form_submit = self.ui.get_element((By.ID, "usersubmit"))
        url_after_submit = env.URL_AUTH_REGISTER if fail else env.URL_AUTH_LOGIN
        self.check.submit_and_check(form_submit, url_after_submit)

    def login(self, remember: bool = True, fail: bool = False):
        """
        logs in the registered mock user.
        :param remember: If True, the login form will have a checkbox to "remember me", defaults to True
        """

        self.ui.nav(env.URL_AUTH_LOGIN)

        form_email = self.ui.get_element((By.CSS_SELECTOR, "input[name='email']"))
        form_password = self.ui.get_element((By.CSS_SELECTOR, "input[name='password']"))
        form_submit = self.ui.get_element((By.CSS_SELECTOR, "input[name='submit']"))
        remember_me = self.ui.get_element((By.CSS_SELECTOR, "input[name='remember']"))

        if remember:
            self.ui.click(remember_me)

        self.ui.input_text(form_email, self.user.email)
        self.ui.input_text(form_password, self.user.password)

        url_after_submit = env.URL_AUTH_LOGIN if fail else env.URL_INDEX
        self.check.submit_and_check(form_submit, url_after_submit)

    def reauth(self, url: str):
        """re-authenticates the user.

        :param url: the subdomain expected to redirected from
        """
        form_email = self.ui.get_element((By.CSS_SELECTOR, "input[name='email']"))
        form_password = self.ui.get_element((By.CSS_SELECTOR, "input[name='password']"))
        form_submit = self.ui.get_element((By.CSS_SELECTOR, "input[name='submit']"))
        self.ui.input_text(form_email, self.user.email)
        self.ui.input_text(form_password, self.user.password)
        self.check.submit_and_check(form_submit, url)

    def logout(self):
        """Logout the user by navigating to the logout page"""
        self.ui.nav(env.URL_AUTH_LOGOUT)
