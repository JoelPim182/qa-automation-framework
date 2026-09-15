from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from exceptions import UnexpectedLoginResult
from config import config


class LoginPage(BasePage):

    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")
    LOGIN_BUTTON = (By.CLASS_NAME, "radius")
    FLASH_MESSAGE = (By.ID, "flash")

    SUCCESSFUL_LOGIN_MESSAGE = "You logged into a secure area!"
    INVALID_USERNAME_MESSAGE = "Your username is invalid!"
    INVALID_PASSWORD_MESSAGE = "Your password is invalid!"

    def enter_username(self, username):
        self.type(self.USERNAME, username)

    def enter_password(self, password):
        self.type(self.PASSWORD, password)

    def click_login(self):
        self.click(self.LOGIN_BUTTON)

    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

        return self.wait_for_login_result()

    def wait_for_login_result(self):
        return self.wait(self.login_result)

    def login_result(self, driver):
        flash_text = driver.find_element(*self.FLASH_MESSAGE).text

        expected_messages = (
            self.SUCCESSFUL_LOGIN_MESSAGE,
            self.INVALID_USERNAME_MESSAGE,
            self.INVALID_PASSWORD_MESSAGE,
        )

        for message in expected_messages:
            if message in flash_text:
                return message

        raise UnexpectedLoginResult(
            f"Unexpected login result: {flash_text}"
        )

    def open(self):
        super().open(config.LOGIN_URL)
        self.wait_until_loaded()

    def wait_until_loaded(self):
        self.wait_for_visible(self.USERNAME)
