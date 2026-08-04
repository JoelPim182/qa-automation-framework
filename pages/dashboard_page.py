from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class wait_until_loaded(BasePage):

    FLASH_MESSAGE = (By.ID, "flash")

    def is_loaded(self):

        self.wait_for_visible(self.FLASH_MESSAGE)
