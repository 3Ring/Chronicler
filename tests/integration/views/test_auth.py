import pytest
import asyncio
from selenium.webdriver.common.by import By

from io import TextIOWrapper
from tests.helpers._async import run_parallel, run_sequence
from tests.helpers.all import chron_url
from tests.integration.startup.mockuser import Mock
from tests.helpers.worker import worker


@pytest.mark.asyncio
async def test_auth(mocks: list[Mock], fp: TextIOWrapper):
    test_queue = asyncio.Queue()
    browser_queue = asyncio.Queue()
    for mock in mocks:
        await browser_queue.put(mock)
    for task in [
        register_assets,
        show_passwords,
        register_link_to_login,
        login_link_to_register,
        anonymous_user_redirected_to_login,
        register_bad_user_names,
        register_bad_emails,
        register_bad_passwords,
        can_register,
        bad_logins,
        fresh_user_is_redirected_to_index_from_reauth,
        login_remember_me,
        user_can_reauth,
        can_logout,
    ]:
        await test_queue.put(task)

    await run_parallel(
        *(
            asyncio.create_task(worker(test_queue, browser_queue, fp))
            for _ in range(len(mocks))
        )
    )


async def register_assets(mock: Mock):
    print("register_assets")
    await mock.nav(chron_url("/register"))
    await run_parallel(
        mock.anon_nav(),
        mock.get_element((By.XPATH, "//input[@name='name']")),
        mock.get_element((By.XPATH, "//input[@name='email']")),
        mock.get_element((By.XPATH, "//input[@name='password']")),
        mock.get_element((By.XPATH, "//input[@name='confirm']")),
        mock.get_element((By.XPATH, "//input[@name='reveal']")),
        mock.get_element((By.XPATH, "//input[@name='usersubmit']")),
    )


async def show_passwords(mock: Mock):
    print("show_passwords")
    await mock.nav(chron_url("/register"))
    password, confirm, reveal = await run_parallel(
        mock.get_element((By.XPATH, "//input[@name='password']")),
        mock.get_element((By.XPATH, "//input[@name='confirm']")),
        mock.get_element((By.XPATH, "//input[@name='reveal']")),
    )
    await run_parallel(
        mock.input(password, "password"),
        mock.input(confirm, "confirm"),
    )
    mock.click(reveal)
    revealed_pw = await mock.get_element((By.XPATH, "//input[@name='password']"))
    assert revealed_pw.get_attribute("type") == "text"
    revealed_confirm = await mock.get_element((By.XPATH, "//input[@name='confirm']"))
    assert revealed_confirm.get_attribute("type") == "text"


async def register_link_to_login(mock: Mock):
    print("register_link_to_login")
    await mock.nav(chron_url("/register"))
    link = await mock.get_element((By.XPATH, "//a[@href='/']"))
    await mock.submit(link, next=chron_url())


async def login_link_to_register(mock: Mock):
    print("login_link_to_register")
    await mock.nav(chron_url("/"))
    link = await mock.get_element((By.XPATH, "//a[@href='/register']"))
    await mock.submit(link, next=chron_url("/register"))


async def anonymous_user_redirected_to_login(mock: Mock):
    print("anonymous_user_redirected_to_login")
    await mock.nav(chron_url("/logout"), next=chron_url("/", next="/logout"))
    await mock.nav(chron_url("/reauth"), next=chron_url("/", next="/reauth"))


async def register_bad_user_names(mock: Mock):
    print("register_bad_user_names")
    bad_names = [
        "",
        " ",
        "       ",
        "B",
        ("test" * 5) + "t",
        "試験",
        "test" + "!@#$%^&*()-=./,'\"",
    ]
    for name in bad_names:
        try:
            mock.name = name
            await mock.register(fail=True)
        except Exception as e:
            print(f"\n\n<<dict {mock.name} failed>>")
            raise e


async def register_bad_emails(mock: Mock):
    print("register_bad_emails")
    bad_emails = [
        "@gmail.com",
        "test",
        "       @gmail.com",
        ("test" * (120 // 3)) + "@gmail.com",
        "t@p.c",
    ]
    i = 3
    for email in bad_emails:
        mock.email = email
        i += 1
        await mock.register(fail=True)


async def register_bad_passwords(mock: Mock):
    print("register_bad_passwords")
    bad_passwords = [
        ("", ""),
        ("         ", "         "),
        ("a", "a"),
        ("testtes", "testtes"),
        ("test" * (100 // 3), "test" * (100 // 3)),
        ("testtest", "testtest1"),
    ]
    i = 3
    for pw, confirm in bad_passwords:
        mock.password, mock.confirm = pw, confirm
        await mock.register(fail=True)


async def can_register(mock: Mock):
    print("can_register")
    await mock.register()
    await mock.anon_nav()


async def bad_logins(mock: Mock):
    print("bad_logins")
    await mock.register()
    bad_logins = [
        ("", ""),
        ("", mock.password),
        (mock.email, ""),
        (mock.email + "1", mock.password),
        (mock.email, mock.password + "1"),
        (mock.email.upper(), mock.password),
        (mock.email, mock.password.upper()),
        (mock.email.lower(), mock.password.lower()),
        (mock.email.upper(), mock.password.upper()),
        (mock.email.lower(), mock.password.upper()),
        (mock.email.upper(), mock.password.lower()),
    ]
    i = 4
    for email, password in bad_logins:
        i += 1
        await mock.login(email=email, password=password, fail=True)


async def fresh_user_is_redirected_to_index_from_reauth(mock: Mock):
    print("fresh_user_is_redirected_to_index_from_reauth")
    await mock.register()
    await mock.login()
    await mock.nav(chron_url("/reauth"), next=chron_url("/index"))


async def login_remember_me(mock: Mock):
    print("login_remember_me")
    await mock.register()
    await mock.login()
    mock.browser.delete_all_cookies()
    await mock.nav(chron_url("/", next=chron_url("/index")))


async def user_can_reauth(mock: Mock):
    print("user_can_reauth")
    await mock.register()
    await mock.login()
    restricted = await mock.forced_to_reauth()
    await mock.reauth(restricted)


async def can_logout(mock: Mock):
    print("can_logout")
    await mock.register()
    await mock.login()
    await mock.logout()
    await mock.login()
