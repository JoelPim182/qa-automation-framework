from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get("https://the-internet.herokuapp.com/login")

username = driver.find_element(By.ID, "username")
password = driver.find_element(By.ID, "password")
login_button = driver.find_element(By.CLASS_NAME, "radius")

username.send_keys("tomsmith")
password.send_keys("SuperSecretPassword!")
login_button.click()

input("Press ENTER to close...")
driver.quit()