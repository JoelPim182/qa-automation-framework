from pages.login_page import LoginPage


def test_valid_login(driver):

    login_page = LoginPage(driver)

    login_page.open()

    dashboard = login_page.login("tomsmith", "SuperSecretPassword!")

    assert dashboard.is_loaded()
