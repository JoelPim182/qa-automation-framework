import pytest

from browser.driver import create_driver
from pages.login_page import LoginPage


@pytest.fixture
def driver():
    driver = create_driver()

    yield driver

    driver.quit()


@pytest.fixture
def login_page(driver):
    login_page = LoginPage(driver)
    login_page.open()
    return login_page
