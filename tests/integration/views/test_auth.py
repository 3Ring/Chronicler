from string import whitespace, punctuation

import pytest
from selenium.webdriver.common.by import By
from tests.integration.auth_actions import (
    forced_to_reauth,
    logout,
    login,
    reauth,
    register,
    forced_to_reauth,
)
from tests.helpers import chron_url, generate_user, alter_dict
from tests.integration.browser import BrowserBase


def test_register_assets(browsers: list[BrowserBase]):
    print("test_register_assets")
    for browser in browsers:
        browser.nav(chron_url("/register"))
        browser.get_element((By.XPATH, "//input[@name='name']"))
        browser.get_element((By.XPATH, "//input[@name='email']"))
        browser.get_element((By.XPATH, "//input[@name='password']"))
        browser.get_element((By.XPATH, "//input[@name='confirm']"))
        browser.get_element((By.XPATH, "//input[@name='reveal']"))
        browser.get_element((By.XPATH, "//input[@name='usersubmit']"))


def test_show_passwords(browsers: list[BrowserBase]):
    print("test_show_passwords")
    for browser in browsers:
        browser.nav(chron_url("/register"))
        password = browser.get_element((By.XPATH, "//input[@name='password']"))
        confirm = browser.get_element((By.XPATH, "//input[@name='confirm']"))
        browser.input(password, "test_password")
        browser.input(confirm, "test_confirm")
        reveal = browser.get_element((By.XPATH, "//input[@name='reveal']"))
        browser.click(reveal)
        revealed_pw = browser.get_element((By.XPATH, "//input[@name='password']"))
        assert revealed_pw.get_attribute("type") == "text"
        revealed_confirm = browser.get_element((By.XPATH, "//input[@name='confirm']"))
        assert revealed_confirm.get_attribute("type") == "text"


def test_register_link_to_login(browsers: list[BrowserBase]):
    print("test_register_link_to_login")
    for browser in browsers:
        link = browser.get_element((By.XPATH, "//a[@href='/']"))
        browser.submit(link, next=chron_url())


def test_login_link_to_register(browsers: list[BrowserBase]):
    print("test_login_link_to_register")
    for browser in browsers:
        link = browser.get_element((By.XPATH, "//a[@href='/register']"))
        browser.submit(link, next=chron_url("/register"))


def test_anonymous_user_redirected_to_login(browsers: list[BrowserBase]):
    print("test_anonymous_user_redirected_to_login")
    for browser in browsers:
        browser.nav(chron_url("/logout"), next=chron_url("/", next="/logout"))
        browser.nav(chron_url("/reauth"), next=chron_url("/", next="/reauth"))


def test_register_bad_user_names(inc, browsers: list[BrowserBase]):
    print("test_register_bad_user_names")
    for browser in browsers:
        user = generate_user(inc)
        bad_names = [
            alter_dict(user, name=""),
            alter_dict(user, name=" "),
            alter_dict(user, name="       "),
            alter_dict(user, name="B"),
            alter_dict(user, name=("test" * 5) + "t"),
            alter_dict(user, name="試験"),
            alter_dict(user, name="test" + punctuation),
        ]
        for name in bad_names:
            try:
                register(browser, name, fail=True)
            except Exception as e:
                print(f"\n\n<<dict {name} failed>>")
                raise e


def test_register_bad_emails(inc, browsers: list[BrowserBase]):
    print("test_register_bad_emails")
    for browser in browsers:
        user = generate_user(inc)
        bad_emails = [
            alter_dict(user, email="@gmail.com"),
            alter_dict(user, email="test"),
            alter_dict(user, email="       @gmail.com"),
            alter_dict(user, email=("test" * (120 // 3)) + "@gmail.com"),
            alter_dict(user, email="t@p.c"),
        ]
        for name in bad_emails:
            try:
                register(browser, name, fail=True)
            except Exception as e:
                print(f"\n\n<<dict {name} failed>>")
                raise e


def test_register_bad_passwords(inc, browsers: list[BrowserBase]):
    print("test_register_bad_passwords")
    for browser in browsers:
        user = generate_user(inc)
        bad_passwords = [
            alter_dict(user, password="", confirm=""),
            alter_dict(user, password="         ", confirm="         "),
            alter_dict(user, password="a", confirm="a"),
            alter_dict(user, password="testtes", confirm="testtes"),
            alter_dict(user, password="test" * (100 // 3), confirm="test" * (100 // 3)),
            alter_dict(user, password="testtest", confirm="testtest1"),
        ]
        for name in bad_passwords:
            try:
                register(browser, name, fail=True)
            except Exception as e:
                print(f"\n\n<<dict {name} failed>>")
                raise e


def test_bad_logins(inc, browsers: list[BrowserBase]):
    print("test_bad_logins")
    for browser in browsers:
        user = generate_user(inc)
        register(browser, user)
        bad_logins = [
            alter_dict(user, email="", password=""),
            alter_dict(user, email="", password=user["password"]),
            alter_dict(user, email=user["email"], password=""),
            alter_dict(user, email=user["email"] + "1", password=user["password"]),
            alter_dict(user, email=user["email"], password=user["password"] + "1"),
            alter_dict(user, email=user["email"].upper(), password=user["password"]),
            alter_dict(user, email=user["email"], password=user["password"].upper()),
            alter_dict(
                user, email=user["email"].lower(), password=user["password"].lower()
            ),
            alter_dict(
                user, email=user["email"].upper(), password=user["password"].upper()
            ),
            alter_dict(
                user, email=user["email"].lower(), password=user["password"].lower()
            ),
        ]
        for name in bad_logins:
            try:
                login(browser, name, fail=True)
            except Exception as e:
                print(f"\n\n<<dict {name} failed>>")
                raise e


def test_can_register(logged_ins: dict):
    print("test_can_register")
    """tests handled by fixture"""
    return


def test_auth_user_redirected_to_login(logged_ins: dict):
    print("test_auth_user_redirected_to_login")
    for browser in logged_ins["browsers"]:
        browser.nav(chron_url("/register"), next=chron_url("/index"))
        browser.nav(chron_url(), next=chron_url("/index"))


def test_fresh_user_is_redirected_to_index_from_reauth(logged_ins: dict):
    print("test_fresh_user_is_redirected_to_index_from_reauth")
    for browser in logged_ins["browsers"]:
        browser.nav(chron_url("/reauth"), next=chron_url("/index"))


def test_login_remember_me(
    relogs: dict["browsers" : list[BrowserBase], "users" : list[dict]]
):
    print("test_login_remember_me")
    for browser, user in zip(relogs["browsers"], relogs["users"]):
        browser.nav(chron_url("/"), next=chron_url("/index"))
        logout(browser)
        login(browser, user, remember=False)
        logout(browser)
        browser.driver.delete_cookie("session")
        browser.nav(chron_url("/"))
        login(browser, user)


def test_user_can_reauth(relogs: dict):
    print("test_user_can_reauth")
    for browser, user in zip(relogs["browsers"], relogs["users"]):
        forced_to_reauth(browser)
        reauth(browser, user)


def test_can_logout(logged_ins: dict):
    print("test_can_logout")
    for browser, user in zip(logged_ins["browsers"], logged_ins["users"]):
        logout(browser)
        login(browser, user)
