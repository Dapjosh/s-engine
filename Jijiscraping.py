from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import json
import time
import csv
import os

options = webdriver.ChromeOptions()

options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36")
options.add_argument("--headless=new")

chromedriver_path = ChromeDriverManager().install()

# Initialize the Chrome driver with options
driver = webdriver.Chrome(chromedriver_path, options=options)

base_url = "https://jiji.ng" 
time.sleep(5)
# itemz = []
# itemtarcount = 10
# previous_height = driver.execute_script("return document.body.scrollHeight")
# # to scrap the entire page use:
# # while True
# while True:
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     time.sleep(5)  #
#     new_height = driver.execute_script("return document.body.scrollHeight")
#     if new_height == previous_height:
#         break
#     previous_height = new_height
    
#     textelements = []
#     wait = WebDriverWait(driver, 10)
#     elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@class, 'b-list-advert-base')]")))

#     for element in elements:
#         href = element.get_attribute("href")
#         full_url = href
#         print(full_url)
#         jijipg = {'URLS':full_url}
#         textelements.append(jijipg)
        
#     itemz.extend(textelements)


# file_name = 'link_lists.csv'
# file_exists = os.path.isfile(file_name)

# with open(file_name, 'a', newline='', encoding='utf-8') as f:
#     writer = csv.DictWriter(f, fieldnames=['URLS'])

#     # Write header only if the file is newly created
#     if not file_exists:
#         writer.writeheader()

#     writer.writerows(itemz)     

time.sleep(10)
# Load the saved cookies from the file
# with open('cookies.json', 'r') as file:
#     cookies = json.load(file)

# Visit the website



with open('cookies.json', 'r') as file:
    cookies = json.load(file)
    
driver.get("https://jiji.ng/real-estate")
  
for cookie in cookies:
    if 'expiry' in cookie:
        del cookie['expiry']  # Remove expiry dates as they can cause issues
    driver.add_cookie(cookie)

# # Add the saved cookies to the browser
# for cookie in cookies:
#     driver.add_cookie(cookie)

# Refresh the page to apply the cookies
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
                

