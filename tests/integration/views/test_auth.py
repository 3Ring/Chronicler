import pytest
from selenium.webdriver.common.by import By

from tests.integration.browser.brands import Browsers
from io import TextIOWrapper
from tests.helpers.all import chron_url, generate_user, alter_dict
from tests.helpers.integration import make_mock, run_parallel, run_sequence
from tests.integration.startup.mockuser import Mock

# def test_register_assets(browsers: list[BrowserActions]):
# def preflight(fp: TextIOWrapper, browser: dict[Browsers, str]):
#     browser, brand = browser["driver"], browser["brand"]
#     return make_mock(fp=fp, browser=browser, brand=brand)


@pytest.mark.asyncio
@pytest.mark.parametrize("mocks", [1], indirect=True)
async def test_register_assets(mocks: list[Mock]):
    print("test_register_assets")
    mock = mocks[0]
    print("TAUTH1.1")
    await mock.nav(chron_url("/register"))
    print("TAUTH1.2")
    await run_parallel(
        mock.get_element((By.XPATH, "//input[@name='name']")),
        mock.get_element((By.XPATH, "//input[@name='email']")),
        mock.get_element((By.XPATH, "//input[@name='password']")),
        mock.get_element((By.XPATH, "//input[@name='confirm']")),
        mock.get_element((By.XPATH, "//input[@name='reveal']")),
        mock.get_element((By.XPATH, "//input[@name='usersubmit']")),
    )
    print("TAUTH1.3")


@pytest.mark.asyncio
@pytest.mark.parametrize("mocks", [1], indirect=True)
async def test_show_passwords(mocks: list[Mock]):
    print("test_show_passwords")
    print("TAUTH2.1")
    mock = mocks[0]
    print("TAUTH2.2")
    await mock.nav(chron_url("/register"))
    print("TAUTH2.3")
    password, confirm, reveal = await run_parallel(
        mock.get_element((By.XPATH, "//input[@name='password']")),
        mock.get_element((By.XPATH, "//input[@name='confirm']")),
        mock.get_element((By.XPATH, "//input[@name='reveal']")),
    )
    print("TAUTH2.4")
    await run_parallel(
        mock.input(password, "test_password"),
        mock.input(confirm, "test_confirm"),
    )
    print("TAUTH2.5")
    mock.click(reveal)
    print("TAUTH2.6")
    revealed_pw = await mock.get_element((By.XPATH, "//input[@name='password']"))
    print("TAUTH2.7")
    assert revealed_pw.get_attribute("type") == "text"
    revealed_confirm = await mock.get_element((By.XPATH, "//input[@name='confirm']"))
    print("TAUTH2.8")
    assert revealed_confirm.get_attribute("type") == "text"


@pytest.mark.asyncio
@pytest.mark.parametrize("mocks", [1], indirect=True)
async def test_register_link_to_login(mocks: list[Mock]):
    print("test_register_link_to_login")
    print("TAUTH3.1")
    mock = mocks[0]
    print("TAUTH3.2")
    await mock.nav(chron_url("/register"))
    print("TAUTH3.3")
    link = await mock.get_element((By.XPATH, "//a[@href='/']"))
    print("TAUTH3.4")
    await mock.submit(link, next=chron_url())
    print("TAUTH3.5")


@pytest.mark.asyncio
@pytest.mark.parametrize("mocks", [1], indirect=True)
async def test_login_link_to_register(mocks: list[Mock]):
    print("test_login_link_to_register")
    print("TAUTH4.1")
    mock = mocks[0]
    print("TAUTH4.2")
    await mock.nav(chron_url("/"))
    print("TAUTH4.3")
    link = await mock.get_element((By.XPATH, "//a[@href='/register']"))
    print("TAUTH4.4")
    await mock.submit(link, next=chron_url("/register"))
    print("TAUTH4.5")


@pytest.mark.asyncio
@pytest.mark.parametrize("mocks", [1], indirect=True)
async def test_anonymous_user_redirected_to_login(mocks: list[Mock]):
    print("test_anonymous_user_redirected_to_login")
    print("TAUTH5.1")
    mock = mocks[0]
    print("TAUTH5.2")
    await mock.nav(chron_url("/logout"), next=chron_url("/", next="/logout"))
    print("TAUTH5.3")
    await mock.nav(chron_url("/reauth"), next=chron_url("/", next="/reauth"))
    print("TAUTH5.4")


@pytest.mark.asyncio
@pytest.mark.parametrize("mocks", [1], indirect=True)
async def test_register_bad_user_names(mocks: list[Mock]):
    print("test_register_bad_user_names")
    print("TAUTH6.1")
    mock = mocks[0]
    print("TAUTH6.2")
    bad_names = [
        "",
        " ",
        "       ",
        "B",
        ("test" * 5) + "t",
        "試験",
        "test" + "!@#$%^&*()-=./,'\"",
    ]
    print("TAUTH6.3")
    for name in bad_names:
        try:
            print("TAUTH6.4")
            mock.name = name
            await mock.register(fail=True)
        except Exception as e:
            print(f"\n\n<<dict {mock.name} failed>>")
            raise e


@pytest.mark.asyncio
@pytest.mark.parametrize("mocks", [1], indirect=True)
async def test_register_bad_emails(mocks: list[Mock]):
    print("test_register_bad_emails")
    mock = mocks[0]
    bad_emails = [
        "@gmail.com",
        "test",
        "       @gmail.com",
        ("test" * (120 // 3)) + "@gmail.com",
        "t@p.c",
    ]
    for email in bad_emails:
        mock.email = email
        await mock.register(fail=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("mocks", [1], indirect=True)
async def test_register_bad_passwords(mocks: list[Mock]):
    print("test_register_bad_passwords")
    mock = mocks[0]
    bad_passwords = [
        ("", ""),
        ("         ", "         "),
        ("a", "a"),
        ("testtes", "testtes"),
        ("test" * (100 // 3), "test" * (100 // 3)),
        ("testtest", "testtest1"),
    ]
    for pw, confirm in bad_passwords:
        mock.password, mock.confirm = pw, confirm
        await mock.register(fail=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("mocks", [1], indirect=True)
async def test_can_register(mocks: list[Mock]):
    print("test_can_register")
    mock = mocks[0]
    await mock.register()


@pytest.mark.asyncio
@pytest.mark.parametrize("mocks", [1], indirect=True)
async def test_bad_logins(mocks: list[Mock]):
    print("test_bad_logins")
    mock = mocks[0]
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
    for email, password in bad_logins:
        await mock.login(email=email, password=password, fail=True)


@pytest.mark.asyncio
@pytest.mark.parametrize("mocks", [1], indirect=True)
async def test_fresh_user_is_redirected_to_index_from_reauth(mocks: list[Mock]):
    print("test_fresh_user_is_redirected_to_index_from_reauth")
    mock = mocks[0]
    await mock.register()
    await mock.login()
    await mock.nav(chron_url("/reauth"), next=chron_url("/index"))


@pytest.mark.asyncio
@pytest.mark.parametrize("mocks", [1], indirect=True)
async def test_login_remember_me(mocks: list[Mock]):
    print("test_login_remember_me")
    mock = mocks[0]
    await mock.register()
    await mock.login()
    await mock.reset()
    await mock.nav(chron_url("/", next=chron_url("/index")))


@pytest.mark.asyncio
@pytest.mark.parametrize("mocks", [1], indirect=True)
async def test_user_can_reauth(mocks: list[Mock]):
    print("test_user_can_reauth")
    mock = mocks[0]
    await mock.register()
    await mock.login()
    restricted = await mock.forced_to_reauth()
    await mock.reauth(restricted)


@pytest.mark.asyncio
@pytest.mark.parametrize("mocks", [1], indirect=True)
async def test_can_logout(mocks: list[Mock]):
    print("test_can_logout")
    mock = mocks[0]
    await mock.register()
    await mock.login()
    await mock.logout()
    await mock.login()
