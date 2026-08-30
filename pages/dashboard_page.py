from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class DashboardPage(BasePage):

    FLASH_MESSAGE = (By.ID, "flash")
    SUCCESSFUL_LOGIN_MESSAGE = "You logged into a secure area!"

    def wait_until_loaded(self):
        self.wait(
            EC.text_to_be_present_in_element(
                self.FLASH_MESSAGE,
                self.SUCCESSFUL_LOGIN_MESSAGE
            )
        )
