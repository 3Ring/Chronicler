import os
from typing import List

from selenium.webdriver.common.by import By

from testing.end_to_end.models import Characters
from testing.end_to_end.helpers import redirect
from testing.end_to_end import Mock
from testing import globals as env

from .join_helpers import joining_primer


def test_anon_user_is_redirected_to_login(mock: Mock):
    with mock.test_manager(test_anon_user_is_redirected_to_login):
        joining_primer(mock)
        url = mock.ui.browser.current_url
        mock.user.auth_logout(mock)
        print(f'url: {url}')
        mock.ui.nav(url, full_url=True)
        redirected = redirect(
            url[len(os.environ.get("ROOT_URL")) :], env.URL_AUTH_LOGIN
        )
        mock.ui.confirm_url(redirected)


def test_joining_assests_with_characters(mock: Mock):
    character_amount = 3
    with mock.test_manager(test_joining_assests_with_characters):
        joining_primer(mock)
        url = mock.ui.browser.current_url
        print(f'url: {url}')
        characters = mock.user.create_characters(mock, amount=character_amount)
        mock.ui.nav(url, full_url=True)
        joining_forms(mock, 2)
        add_form(mock, characters)
        create_form(mock)


def test_joining_assests_without_characters(mock: Mock):
    with mock.test_manager(test_joining_assests_without_characters):
        joining_primer(mock)
        joining_forms(mock, 1)
        create_form(mock)
        
# 
# Helpers
# 


def joining_forms(mock: Mock, amount: int):
    forms = mock.ui.get_all_elements((By.TAG_NAME, "form"))
    assert len(forms) == amount
    for form in forms:
        assert form.is_displayed()
    headers = mock.ui.get_all_elements((By.TAG_NAME, "h1"))
    HEADERS = ["Add Character From Your Characters", "Create a New Character!"]
    assert True in [any([h.text.find(H) for H in HEADERS]) for h in headers]


def create_form(mock: Mock):
    """confirms create_character_form assets"""
    assets = [
        mock.ui.get_element((By.CSS_SELECTOR, "label[for='create-name']")),
        mock.ui.get_element(
            (By.CSS_SELECTOR, "input[type='text'][name='create-name']")
        ),
        mock.ui.get_element((By.CSS_SELECTOR, "label[for='create-img']")),
        mock.ui.get_element((By.CSS_SELECTOR, "input[type='file'][name='create-img']")),
        mock.ui.get_element((By.CSS_SELECTOR, "label[for='create-bio']")),
        mock.ui.get_element((By.CSS_SELECTOR, "textarea[name='create-bio']")),
        mock.ui.get_element(
            (By.CSS_SELECTOR, "input[type='submit'][name='create-submit']")
        ),
    ]
    for element in assets:
        assert element.is_displayed


def add_form(mock: Mock, characters: List[Characters]):
    """confirms add_character_form assets"""
    submit_selector = (By.CSS_SELECTOR, "input[type='submit'][value='Add to Game']")
    assets = [mock.ui.get_element(submit_selector)]
    character_options = mock.ui.get_all_elements(
        (By.CSS_SELECTOR, "input[name='add-character']")
    )
    assert len(character_options) == len(characters)
    names = [c.name for c in characters]
    for option in character_options:
        label_selector = (By.CSS_SELECTOR, f"label[for='{option.get_attribute('id')}']")
        label = mock.ui.get_element(label_selector)
        assert True in [(label.text.find(name) != -1) for name in names]
        assets.append(option)
        assets.append(label)
    for element in assets:
        assert element.is_displayed
