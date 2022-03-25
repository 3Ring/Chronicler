from tests.helpers import chron_url
from selenium.webdriver.common.by import By
from tests.integration.browser import BrowserBase

def register(browser: BrowserBase, user: dict, fail: bool = False):

    print(f'browser in register: {browser}')
    print(f'r1')
    browser.nav(chron_url("/register"))
    print(f'r2')
    
    reg_name = browser.get_element((By.XPATH, "//input[@name='name']"))
    print(f'r3')
    reg_email = browser.get_element((By.XPATH, "//input[@name='email']"))
    reg_password = browser.get_element((By.XPATH, "//input[@name='password']"))
    reg_confirm = browser.get_element((By.XPATH, "//input[@name='confirm']"))
    reg_form_submit = browser.get_element((By.XPATH, "//input[@name='usersubmit']"))
    browser.input(reg_name, user["name"])
    browser.input(reg_email, user["email"])
    browser.input(reg_password, user["password"])
    browser.input(reg_confirm, user["confirm"])
    print(f'r4')
    if fail: 
        browser.submit(reg_form_submit, next=chron_url("/register"))
    else:
        browser.submit(reg_form_submit, next=chron_url())
    print(f'r5')
    return browser


def login(register: BrowserBase, user: dict, remember: bool = True, fail: bool = False):

    print(f'L1')
    register.nav(chron_url())
    print(f'L2')
    login_email = register.get_element((By.XPATH, "//input[@name='email']"))
    login_password = register.get_element((By.XPATH, "//input[@name='password']"))
    login_submit = register.get_element((By.XPATH, "//input[@name='submit']"))
    if remember:
        remember_me = register.get_element((By.XPATH, "//input[@name='remember']"))
        remember_me.click()
    register.input(login_email, user["email"])
    register.input(login_password, user["password"])
    print(f'L3')
    if fail:
        register.submit(login_submit, next=chron_url())
    else:
        register.submit(login_submit, next=chron_url("/index"))
    print(f'L4')
    return register


def reauth(logged: BrowserBase, user: dict, remember: bool = True):
    email = logged.get_element((By.XPATH, "//input[@name='email']"))
    password = logged.get_element((By.XPATH, "//input[@name='password']"))
    submit = logged.get_element((By.XPATH, "//input[@name='submit']"))
    if remember:
        r = logged.get_element((By.XPATH, "//input[@name='submit']"))
        logged.click(r)
    logged.input(email, user["email"])
    logged.input(password, user["password"])
    logged.submit(submit, next=chron_url("/edit/account"))


def logout(browser: BrowserBase):
    """
    Log out new user

    :param browser: The browser object to log out
    :return: The browser object.
    """
    browser.nav(chron_url("/logout"), next=chron_url())
    return browser


def forced_to_reauth(browser: BrowserBase):
    browser.nav(chron_url("/profile/account"))
    edit = browser.get_element((By.XPATH, "//a[@href='/edit/account']"))
    browser.submit(edit, next=chron_url("/reauth", next="/edit/account"))
