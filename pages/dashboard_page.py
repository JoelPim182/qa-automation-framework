from pages.base_page import BasePage


class DashboardPage(BasePage):

    def is_loaded(self):
        return self.current_url().endswith("/secure")
