from selenium.webdriver.common.by import By

from testing.end_to_end import Mock
from testing.end_to_end.helpers import redirect
from testing import globals as env
from testing.end_to_end.tests.asset_helpers import (
    asset_validator_by_tag,
    asset_validator_by_css,
    assets_validator_by_css,
    validate_list,
    get_nested_element,
)


def test_index_redirects_anon_user_to_login(mock: Mock):
    with mock.test_manager(test_index_redirects_anon_user_to_login):
        mock.ui.nav(env.URL_INDEX)
        mock.ui.confirm_url(redirect(env.URL_INDEX, env.URL_AUTH_LOGIN))


def test_index_page_assets(mock: Mock):
    with mock.test_manager(test_index_page_assets):
        mock.user.register_and_login(mock)
        mock.ui.confirm_url(env.URL_INDEX)
        mock.ui.nav_is_authenticated()
        asset_validator_by_tag(mock, "h1", text_to_check="Welcome!")
        asset_validator_by_tag(mock, "h2", text_to_check="DUNGEON MASTER")
        asset_validator_by_tag(mock, "h2", text_to_check="PLAYER")
        asset_validator_by_css(mock, f'div.games a[href="{env.URL_CREATE_GAME}"]')
        asset_validator_by_css(mock, f'div.games a[href="{env.URL_JOIN}"]')
        asset_validator_by_tag(
            mock, "p", text_to_check="You don't appear to have created any games yet."
        )
        asset_validator_by_tag(
            mock, "p", text_to_check="You don't appear to have joined any games yet."
        )


def test_with_games(mock: Mock):
    with mock.test_manager(test_with_games):
        mock.user.register_and_login(mock)
        game1 = mock.user.create_game_and_dm(mock)
        mock.add_user()
        mock.user.register_and_login(mock)
        game2 = mock.user.create_game_and_dm(mock)
        mock.user.join_game_with_create(mock, game1)
        mock.ui.nav(env.URL_INDEX)
        headers = assets_validator_by_css(mock, 2, "div.game")
        for div in headers:
            header = get_nested_element(div, (By.TAG_NAME, "h2"))
            if header.text.find("DUNGEON MASTER") != -1:
                dm_header = div
            elif header.text.find("PLAYER") != -1:
                player_header = div
        dm_subtitle = get_nested_element(dm_header, (By.TAG_NAME, "p"))
        validate_list([dm_subtitle], 1, False, "These are games you have created.")
        dm_game = get_nested_element(dm_header, (By.TAG_NAME, "h3"))
        validate_list([dm_game], 1, False, game2.name)
        player_subtitle = get_nested_element(player_header, (By.TAG_NAME, "p"))
        validate_list(
            [player_subtitle], 1, False, "These are games you have joined as a player."
        )
        player_game = get_nested_element(player_header, (By.TAG_NAME, "h3"))
        validate_list([player_game], 1, False, game1.name)
