from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import logging
from time import sleep
import pickle
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-popup-blocking")

driver = webdriver.Chrome()
logging.info("Chrome launched")

driver.maximize_window()
logging.info("Chrome with facebook maximized")

driver.get("https://www.facebook.com/")

if os.path.exists('cookies.pkl'):
    logging.info("loading cookies to bypass login...")
    with open('cookies.pkl', 'rb') as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)
    driver.refresh()

try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[aria-label='Facebook']"))
    )
    logging.info("Facebook is logged in successfully")

except Exception as e:
    login = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#email"))
    )
    with open('details.txt', 'r') as file:
        details_info = file.readlines()
    login.send_keys(details_info[0].strip())
    logging.info("Email or phone number added")

    password = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#pass"))
    )
    password.send_keys(details_info[1].strip())

    driver.find_element(By.CSS_SELECTOR, "button[name='login']").click()
    logging.info("Login clicked success")

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '(//div[@aria-hidden="false"])[21]'))
        ).is_displayed()
        logging.info("save login info is displayed")
        driver.find_element(By.CSS_SELECTOR, "div[aria-label='Close'").click()
        logging.info("Closed login info")
        logging.info("logged in success fully")
    except:
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "img[src*='captcha']"))
            )
            logging.warning("Captcha detected solve it manually")
            input("Please enter captcha manually and enter here")
        except Exception as e:
            logging.info("No Captcha detected", e)

        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[aria-label='Facebook'"))
            )
            logging.info("Logged in successfully")

            pickle.dump(driver.get_cookies(), open('cookies.pkl', 'wb'))
            logging.info("Cookies saved for future logins")
        except Exception as e:
            logging.error("Login failed", e)

sleep(5)
try:
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div[aria-label='Your profile']"))
    ).click()
    logging.info("Clicked successfully logout profile ")
except Exception as e:
    logging.error("Failed to click logout profile", e)

try:
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Log Out']"))
    ).click()
    logging.info("Successfully clicked Log out button")
except Exception as e:
    logging.error("Failed to logout", e)

finally:
    sleep(2)
    driver.quit()
    logging.info("Browser closed.")

