from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import config


class BasePage:

    def __init__(self, driver):
        self.driver = driver

    def current_url(self):
        return self.driver.current_url

    def find(self, locator):
        return self.driver.find_element(*locator)

    def click(self, locator):
        self.find(locator).click()

    def type(self, locator, text):
        self.find(locator).send_keys(text)

    def wait(self, condition, timeout=config.DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(condition)

    def open(self, url):
        self.driver.get(url)

    def wait_for_visible(self, locator, timeout=config.DEFAULT_TIMEOUT):
        return self.wait(
            EC.visibility_of_element_located(locator),
            timeout
        )
