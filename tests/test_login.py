from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


def test_valid_login(driver):

    login_page = LoginPage(driver)

    login_page.open()

    result = login_page.login("tomsmith", "SuperSecretPassword!")

    assert result == LoginPage.SUCCESSFUL_LOGIN_MESSAGE

    dashboard = DashboardPage(driver)
    dashboard.wait_until_loaded()


def test_invalid_password(driver):

    login_page = LoginPage(driver)

    login_page.open()

    result = login_page.login("tomsmith", "invalid-password")

    assert result == LoginPage.INVALID_PASSWORD_MESSAGE

def test_invalid_username(driver):

    login_page = LoginPage(driver)

    login_page.open()

    result = login_page.login("invalid-username", "SuperSecretPassword!")

    assert result == LoginPage.INVALID_USERNAME_MESSAGE

