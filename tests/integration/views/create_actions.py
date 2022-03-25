from tests.helpers import chron_url, generate_game
from selenium.webdriver.common.by import By
from tests.integration.browser import BrowserBase
from selenium.webdriver.remote.webelement import WebElement
from project.helpers.misc import bool_convert
def create_game(logged_in: BrowserBase, game: dict, dm_name: bool = None) -> None:
    print(f'c1')
    logged_in.nav(chron_url("/create/game"))
    print(f'c2')
    name = logged_in.get_element((By.ID, "name"))
    print(f'c3')
    logged_in.input(name, game["name"])
    pub = logged_in.get_element((By.XPATH, "//input[@name='published']"))
    print(f'c4')
    if game["publish"]:
        logged_in.click(pub)
    # print(f'pub.get_attribute("value"): {pub.get_attribute("checked")}')
    # print(f'game: {game}')
    print(f'c5')
    assert bool_convert(pub.get_attribute("checked")) == game["publish"]
    game_submit = logged_in.get_element((By.XPATH, "//input[@name='gamesubmit']"))
    print(f'c6')
    logged_in.submit(game_submit, next=chron_url("/create/dm"), partial_url=True)
    print(f'c7')
    create_dm(logged_in, game, dm_name)
    print(f'c8')


def create_dm(game_created: BrowserBase, game: dict, dm_name: bool = None) -> None:
    if dm_name is not None:
        name = game_created.get_element((By.XPATH, "//input[@name='name']"))
        game_created.input(name, dm_name)
    dm_submit = game_created.get_element((By.ID, "submit"))
    print(f'd1')
    game_created.submit(dm_submit, next=chron_url("/notes"), partial_url=True)
    print(f'd2')
    print(f'game_created.driver.current_url: {game_created.driver.current_url}')

