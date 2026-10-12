from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class DashboardPage(BasePage):

    DASHBOARD_HEADING = (By.XPATH, "//h2[normalize-space()='Secure Area']")

    def wait_until_loaded(self):
        self.wait_for_visible(self.DASHBOARD_HEADING)
