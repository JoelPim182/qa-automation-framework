import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from unittest.mock import Mock
from exceptions import UnexpectedLoginResult


def test_valid_login(login_page):

    result = login_page.login("tomsmith", "SuperSecretPassword!")

    assert result == LoginPage.SUCCESSFUL_LOGIN_MESSAGE

    dashboard = DashboardPage(login_page.driver)
    dashboard.wait_until_loaded()


@pytest.mark.parametrize(
    "username, password, expected_result",
    [
        pytest.param(
            "tomsmith",
            "invalid-password",
            LoginPage.INVALID_PASSWORD_MESSAGE,
            id="invalid_password"
        ),
        pytest.param(
            "invalid-username",
            "SuperSecretPassword!",
            LoginPage.INVALID_USERNAME_MESSAGE,
            id="invalid_username"
        )
    ]
)
def test_invalid_login(login_page, username, password, expected_result):

    result = login_page.login(username, password)

    assert result == expected_result


def test_unexpected_login_result():
    driver = Mock()
    driver.find_element.return_value.text = "Something unexpected happened"

    login_page = LoginPage(driver)

    with pytest.raises(UnexpectedLoginResult):
        login_page.login_result(driver)
