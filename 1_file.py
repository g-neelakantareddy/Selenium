from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.get("https://www.tutorialspoint.com/index.htm")
driver.maximize_window()

driver.find_element(By.CLASS_NAME, "search-input").send_keys("Python")
sleep(1)
driver.find_element(By.CLASS_NAME, "nav__signup-link").click()
signin_page = driver.title
if signin_page == "Login - Video Courses, eBooks, Certifications | Tutorialspoint":
    driver.find_element(By.ID, "login_email").send_keys("gneelakantareddy143@gmail.com")
    driver.find_element(By.ID, "login_password").send_keys("143neela@")
    driver.find_element(By.ID, "sign_in_btn").click()

input("Please enter to exit")
