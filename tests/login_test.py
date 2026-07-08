from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get("https://the-internet.herokuapp.com/login")

username = driver.find_element(By.ID, "username")
password = driver.find_element(By.ID, "password")
login_button = driver.find_element(By.CLASS_NAME, "radius")

username.send_keys("tomsmith")
password.send_keys("SuperSecretPassword!")
login_button.click()

wait = WebDriverWait(driver, 10)

message = wait.until(
    EC.visibility_of_element_located((By.ID, "flash"))
)

#message = driver.find_element(By.ID, "flash")

#commit

assert "You logged into a secure area!" in message.text
#assert "Joel" in message.text

input("Press ENTER to close...")
driver.quit()