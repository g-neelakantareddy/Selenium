from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import logging
from time import sleep
import imaplib
import email
import re

logging.basicConfig(
    filename=r'C:/Users/neelakanta.reddy/SecondPhase/Selenium/log_file.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w',
)

driver = webdriver.Chrome()

driver.get("https://ttdevasthanams.ap.gov.in/home/dashboard")
driver.maximize_window()
logging.info("Window maximized")

login = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Log In']"))
)
login.click()
logging.info("Clicked login button successfully")

login_page_displayed = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH,
                                    "//body/div[@id='__next']/div/div[@role='dialog']/div[@class='login_dialogMobileBody__tgMsH']/div[1]"))
)
login_page_displayed.is_displayed()
logging.info("Displayed_login_pop")

enter_mobile_number = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']//div[2]//div[1]//input[1]"))
)
enter_mobile_number.send_keys("9866242188")

driver.find_element(By.XPATH, "//button[normalize-space()='Get OTP']").click()

EMAIL_USER = "gneelakantareddy4143@gmail.com"
EMAIL_PASS = "bcvvtoqmigslpjoi"


def get_otp_from_email():
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("inbox")

        status, data = mail.search(None, "ALL")
        mail_ids = data[0].split()

        for num in mail_ids[::-1]:  # Check latest emails first
            status, data = mail.fetch(num, "(RFC822)")
            msg = email.message_from_bytes(data[0][1])

            if "OTP" in msg.get_payload():  # Adjust keyword as needed
                otp_match = re.search(r"\b\d{6}\b", msg.get_payload())
                if otp_match:
                    return otp_match.group()

        mail.logout()
    except Exception as e:
        print("Error fetching OTP:", e)
    return None


sleep(10)
otp = get_otp_from_email()
a, b, c, d, e, f = otp

driver.find_element(By.XPATH,
                    "//body//div[@id='__next']//div[@class='login_innerDiv__tK53z']//div//div//div[1]//div[1]//input[1]").send_keys(
    a)
driver.find_element(By.XPATH, "//div[@role='dialog']//div[2]//div[1]//input[1]").send_keys(b)
driver.find_element(By.XPATH, "//div[3]//div[1]//input[1]").send_keys(c)
driver.find_element(By.XPATH, "//div[4]//div[1]//input[1]").send_keys(d)
driver.find_element(By.XPATH, "//div[5]//div[1]//input[1]").send_keys(e)
driver.find_element(By.XPATH, "//div[6]//div[1]//input[1]").send_keys(f)

driver.find_element(By.XPATH, "//button[normalize-space()='Login']").click()

ammavari_darshan_ticket = WebDriverWait(driver, 60).until(
    EC.element_to_be_clickable((By.XPATH, "//div[5]//div[1]//img[1]"))
)
ammavari_darshan_ticket.click()

input("wait")
driver.quit()
