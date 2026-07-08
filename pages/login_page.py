from selenium.webdriver.common.by import By


class LoginPage:

    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")
    LOGIN_BUTTON = (By.CLASS_NAME, "radius")

    def __init__(self, driver):
        self.driver = driver
