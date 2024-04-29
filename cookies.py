from datetime import datetime, timedelta
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import json

# options = webdriver.ChromeOptions()

options = webdriver.ChromeOptions()
# session = requests.session()
chromedriver_path = ChromeDriverManager().install()
service = Service(executable_path=chromedriver_path)
base_url = "https://jiji.ng"
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36")
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
# options = {
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
#     "args": ["--headless=new"],
#     "no-sandbox": True,
# }

# Initialize the Chrome driver with options
driver = webdriver.Chrome(service=service, options=options)
# driver = session.get(webdriver.Chrome,service=service, options=options)

driver.get(base_url)

# Locate the "Sign In" link using the given XPath
sign_in_link = driver.find_element(By.XPATH, "//a[@href='/login.html' and @class='h-flex-center']")

# Click on the "Sign In" link
sign_in_link.click()

# Wait for the presence of the email or phone input field
wait = WebDriverWait(driver, 30)
email_phone_input = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'E-mail or phone')]")))

# Click on the "E-mail or phone" input field
email_phone_input.click()

# Input the email or phone number
emailinput = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@class, 'qa-login-field')]")))
emailinput.send_keys("daposhiyanbola@gmail.com")

# Locate the password input field and input the password
password_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']")))
password_input.send_keys("JohnBull!23")

# Locate and click the "Log in" button
login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'SIGN IN')]")))
login_button.click()
time.sleep(5)


driver_cookies = driver.get_cookies()

expiration_time = int((datetime.now() + timedelta(days=30)).timestamp()) 

for cookie in driver_cookies:
    cookie['expiry'] = expiration_time
    
SESSION_COOKIES_JSON = json.dumps(driver_cookies)

os.environ['SESSION_COOKIES'] = SESSION_COOKIES_JSON

driver.quit()
