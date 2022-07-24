from typing import List, Tuple

from functools import partial

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from testing import exceptions as ex
from testing.end_to_end import Mock


def _get_assets(
    by: str,
    mock: Mock,
    amount: int,
    selector: str,
    text_to_check: str = None,
    hidden: bool = False,
) -> List[WebElement]:
    elements = mock.ui.get_all_elements((by, selector))
    return validate_list(elements, amount, hidden, text_to_check)


assets_validator_by_tag = partial(_get_assets, By.TAG_NAME)
assets_validator_by_id = partial(_get_assets, By.ID)
assets_validator_by_css = partial(_get_assets, By.CSS_SELECTOR)


def asset_validator_by_id(
    mock: Mock, id: str, text_to_check: str = None, hidden: bool = False
) -> WebElement:
    return assets_validator_by_id(
        mock=mock, selector=id, amount=1, text_to_check=text_to_check, hidden=hidden
    )[0]


def asset_validator_by_tag(
    mock: Mock, tag: str, text_to_check: str = None, hidden: bool = False
) -> WebElement:
    return assets_validator_by_tag(
        mock=mock, selector=tag, amount=1, text_to_check=text_to_check, hidden=hidden
    )[0]


def asset_validator_by_css(
    mock: Mock, css_selector: str, text_to_check: str = None, hidden: bool = False
) -> WebElement:
    return assets_validator_by_css(
        mock=mock,
        selector=css_selector,
        amount=1,
        text_to_check=text_to_check,
        hidden=hidden,
    )[0]


def get_nested_element(element: WebElement, locator: Tuple[By, str]) -> WebElement:
    try:
        return element.find_element(*(arg for arg in locator))
    except NoSuchElementException:
        raise ex.ElementNotFoundError(
            f"unable to find element by locator {locator} nested inside {element}"
        )


def validate_list(
    elements: List[WebElement],
    amount: int,
    hidden: bool,
    text_to_check: str = None,
) -> List[WebElement]:
    if text_to_check is None:
        filtered = elements
    else:
        filtered = []
        for el in elements:
            if el.text.find(text_to_check) != -1:
                filtered.append(el)
    try:
        assert len(filtered) == amount
    except AssertionError:
        if text_to_check is not None:
            raise ex.ExpectedTextNotFoundError(
                f"{text_to_check}, of amount: {amount}, not found in {[e.text for e in elements]}"
            )
        raise ex.ExpectedAmountError(
            f"amount: {amount} != len(filtered): {len(filtered)}"
        )
    for el in filtered:
        assert el.is_displayed() if not hidden else not el.is_displayed()
    return filtered
