class BasePage:

    def __init__(self, driver):
        self.driver = driver

    def current_url(self):
        return self.driver.current_url
