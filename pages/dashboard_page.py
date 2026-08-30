from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class DashboardPage(BasePage):

    FLASH_MESSAGE = (By.ID, "flash")
    SUCCESSFUL_LOGIN_MESSAGE = "You logged into a secure area!"
    DASHBOARD_HEADING = (By.XPATH, "//h2[normalize-space()='Secure Area']")

    def wait_until_loaded(self):
        self.wait_for_visible(self.DASHBOARD_HEADING)
