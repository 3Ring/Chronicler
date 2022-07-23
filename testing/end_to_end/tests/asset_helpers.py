from typing import List

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

from testing.end_to_end import Mock


def assets_by_css_validator(
    mock: Mock, amount: int, selector: str, text_to_check: str = None
) -> List[WebElement]:
    elements = mock.ui.get_all_elements((By.CSS_SELECTOR, selector))
    return _validator(elements, amount, text_to_check)


def assets_by_tag_validator(
    mock: Mock, amount: int, tag: str, text_to_check: str = None
) -> List[WebElement]:
    """helper function to find all elements with a given tag name and assert there is the correct amount"""
    elements = mock.ui.get_all_elements((By.TAG_NAME, tag))
    return _validator(elements, amount, text_to_check)


def _validator(
    elements: List[WebElement], amount: int, text_to_check: str = None
) -> List[WebElement]:
    if text_to_check is None:
        filtered = elements
    else:
        filtered = []
        for el in elements:
            if el.text.find(text_to_check) != -1:
                filtered.append(el)
    assert len(filtered) == amount
    for el in filtered:
        assert el.is_displayed
    return filtered
