from selenium import webdriver
from datetime import datetime, timedelta
from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import requests
import pickle
import json
import time
import csv
import os

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

driver.get(base_url)

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

username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")
emailinput.send_keys(username)

# Locate the password input field and input the password
password_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']")))
password_input.send_keys(password)

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

 
session_cookies_json = os.environ.get('SESSION_COOKIES')
session_cookies = json.loads(session_cookies_json)

headers= {}

test = requests.get(base_url, headers=headers, cookies=session_cookies)

driver.refresh()

time.sleep(5)

existing_seller_names = set()
existing_phone_numbers = set()

seller_info_list = []

count = 1
 
with open('link_lists.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the header row if it exists
    for row in reader:
        seller_url = row[0]
        driver.get(seller_url)
        time.sleep(5) 

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//body")))
        
        current_url = driver.current_url
        if not current_url == seller_url:
            print(f"Redirected from {seller_url} to {current_url}")
            # Handle redirection if necessary, or continue to the next URL
            continue
        
        try:
            showcon = "//div[contains(@class, 'b-button') and contains(text(), 'Show contact')]"
            show_contact_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, showcon))
            )
            driver.execute_script("arguments[0].scrollIntoView();", show_contact_element)
            show_contact_element.click()
             
        except TimeoutException:
            print(f"Timeout occurred for URL: {seller_url}")
            continue  # Skip this entry and continue with the next one
        except NoSuchElementException:
            print(f"Required elements not found in URL: {seller_url}")
            continue  # Skip this entry and continue with the next one
        except Exception as e:
            print(f"An error occurred while processing {seller_url}: {e}")
        
        # driver.execute_script("arguments[0].scrollIntoView();", show_contact_element)
        # num = WebDriverWait(driver, 30).until(
        # EC.presence_of_element_located((By.XPATH, showcon))
        # )
        # num.click()
        phone_number_text = "Phone number not available"
        xpath1 = "//div[@class='b-show-contacts-popover-item__phone h-flex-1-0 h-mr-15']"
        # XPath for the second DOM structure
        xpath2 = "//div[contains(@class, 'h-flex-center b-btn') and contains(@class, 'h-font-weight-500')]"
        
        try:
            # Try to find the phone number using the first DOM structure
            phone_number_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath1))
            )
            phone_number_text = phone_number_element
        except TimeoutException:
            # If the first attempt fails, try the second DOM structure
            try:
                phone_number_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, xpath2))
                )
                phone_number_text = phone_number_element
            except TimeoutException:
                # If both attempts fail, handle as phone number not available
                pass
        
    
        # phone_number_text = None
     
        # phone_number = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//div[@class='b-show-contacts-popover-item__phone h-flex-1-0 h-mr-15']"))
        # )
        # if phone_number !=None:
        #     phone_number_text = phone_number
        # else:
        #     phone_number_text = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//div[@class='h-flex-center b-btn h-font-weight-500 b-btn--main h-height-40 h-width-100p']"))
        # )  
        
            
        SellerName = driver.find_element(By.XPATH, "//div[@class='b-seller-block__name']")
        city = driver.find_element(By.XPATH, "//div[@class='b-advert-info-statistics']")
        
        # Cost = driver.find_element(By.XPATH, "//span[@class='qa-advert-price-view-title b-alt-advert-price__text']")

        if SellerName.text in existing_seller_names or phone_number_text.text in existing_phone_numbers:
            continue  # Skip the rest of the loop and move to the next iteration

        # Add the new SellerName and PhoneNumber to the sets
        
        existing_seller_names.add(SellerName.text)
        
        existing_phone_numbers.add(phone_number_text.text)
        
        jijipg = {
                        'S/N' : count,
                        'SellerName': SellerName.text,
                        'City': city.text,
                        # 'Price': Cost.text,
                        'PhoneNumber': phone_number_text.text
                    }
        print(jijipg)
        count = count+1
        seller_info_list.append(jijipg)
       
        if count % 1000 == 0:
            file_name = f'seller_info_{count}.csv'
            with open(file_name, 'w', newline='', encoding='utf-8') as f:
                fieldnames = ['S/N','SellerName', 'Price', 'PhoneNumber']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(seller_info_list)
                seller_info_list.clear()
            print(f"CSV file {file_name} created")
        
print(len(seller_info_list))

# file_name = 'seller_info.csv'

# with open(file_name, 'w', newline='', encoding='utf-8') as f:
#     fieldnames = ['S/N','SellerName', 'City', 'Price', 'PhoneNumber']
#     writer = csv.DictWriter(f, fieldnames=fieldnames)
#     writer.writeheader()
#     writer.writerows(seller_info_list)

# Quit the browser
driver.quit()       
                

