from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import logging
import re
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

# Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-popup-blocking')

# Logger setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)
logging.info('Chrome opened successfully')

driver.maximize_window()
logging.info('Chrome maximized successfully')

# Navigate to the page
driver.get("https://the-internet.herokuapp.com/")
logging.info('Link open successfully')

try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.heading'))
    )
    logging.info('Page opened successfully')

    # Navigate to Challenging DOM
    driver.find_element(By.CSS_SELECTOR, "a[href='/challenging_dom']").click()

    for index in range(3):  # Iterate over 3 buttons dynamically
        try:
            # Re-locate the buttons after each iteration
            all_elements = driver.find_elements(By.CSS_SELECTOR, 'div.large-2 a')

            if index < len(all_elements):
                button = all_elements[index]

                # Click the button
                button.click()
                logging.info(f"Clicked button {index + 1}")

                # Wait for DOM to stabilize
                WebDriverWait(driver, 5).until(EC.staleness_of(button))

                # Wait for new DOM state
                sleep(2)

                # Retry locating the <script> element
                for _ in range(3):  # Retry loop for stale script element
                    try:
                        script_element = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, "//script[contains(text(), 'Answer')]"))
                        )

                        script_text = script_element.get_attribute('innerHTML')
                        print(f"Script Text: {script_text}")

                        # Extract the answer using regex
                        match = re.search(r"Answer:\s*(\d+)", script_text)

                        if match:
                            answer = match.group(1)
                            print(f"Answer: {answer}")
                            logging.info(f"Answer found: {answer}")
                        else:
                            print("Answer not found!")

                        break  # Exit retry loop if successful

                    except StaleElementReferenceException:
                        print("Stale script element, retrying...")
                        sleep(1)  # Wait before retrying

            else:
                logging.warning(f"No button found at index {index}")

        except Exception as e:
            logging.error(f"Error occurred on button {index + 1}: {e}")

except Exception as e:
    logging.error(f"An error occurred: {e}")

finally:
    driver.quit()
    logging.info("Browser closed.")
