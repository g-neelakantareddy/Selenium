from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import logging
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pyautogui
import re
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.select import Select


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-popup-blocking')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

driver = webdriver.Chrome()
logging.info('Chrome opened successfully')

driver.maximize_window()
logging.info('Chrome maximized successfully')

driver.get("https://the-internet.herokuapp.com/")
logging.info('Link open successfully')
try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.heading'))
    ).displayed()
    logging.info('Page opened successfully')
except Exception as e:
    logging.error('Something went wrong in finding name', e)


def close_browser():
    input('wait..')
    sleep(3)
    logging.info(f'Closed browser')
    driver.quit()


def a_b_testing():
    try:
        print(f"A/B Testing")
        driver.find_element(By.CSS_SELECTOR, 'a[href="/abtest"]').click()
        logging.info('A/B Testing clicked successfully')

        ab_text_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.example h3'))
        )
        ab_text = ab_text_element.text
        logging.info(f'Text is -- {ab_text}')
        sleep(2)
        driver.back()
        logging.info(f'Back to main page')
    except Exception as e:
        logging.error('Something went wrong', e)
    return True


def add_remove_elements():
    # add remove elements
    try:
        print(f"Add Remove Elements")
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/add_remove_elements/"'))
        ).click()
        logging.info(f'add remove button find and clicked')
    except Exception as e:
        logging.error(f"Something went wrong {e}")
    try:
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[onclick="addElement()"'))
        ).click()
        logging.info(f"Clicked on add element button")
        sleep(1)
        driver.find_element(By.CSS_SELECTOR, 'button.added-manually').click()
        logging.info(f'Clicked on get element button')
        sleep(1)
        driver.back()
    except Exception as e:
        logging.info(f"Something went wrong {e}")


def basic_auth():
    # Basic auth
    try:
        print(f"Basic Auth")
        driver.find_element(By.CSS_SELECTOR, 'a[href="/basic_auth"]').click()
        logging.info(f"Clicked on basic authentication")
        sleep(1)
        driver.get('https://admin:admin@the-internet.herokuapp.com/basic_auth')
        text_basic_auth = driver.find_element(By.CSS_SELECTOR, "div.example p").text

        assert "Congratulations" in text_basic_auth
        logging.info('Successfully logged in')
        sleep(2)
        driver.back()
        driver.back()
    except Exception as e:
        logging.info(f"An error occurred : {e}")


def broken_images():
    # Broken Images
    try:
        print(f"Broken images")
        driver.find_element(By.CSS_SELECTOR, 'a[href="/broken_images"]').click()
        images = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.example img'))
        )
        for index, img in enumerate(images, start=1):
            img_src = img.get_attribute('src')
            logging.info(f"Index:{index}, Source:{img_src}")
            if img.is_displayed():
                logging.info(f"Image is displayed")
            else:
                logging.info(f"Image is not displayed")
        logging.info(f"All images are displayed")
        sleep(2)
        driver.back()
    except Exception as e:
        logging.info(f"An error occurred: {e}")


def challenging_dom():
    # Challenging DOM
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.heading'))
        )
        logging.info('Page opened successfully')
        driver.find_element(By.CSS_SELECTOR, "a[href='/challenging_dom']").click()

        for index in range(3):  # Iterate over 3 buttons dynamically
            try:
                all_elements = driver.find_elements(By.CSS_SELECTOR, 'div.large-2 a')

                if index < len(all_elements):
                    button = all_elements[index]
                    button.click()
                    logging.info(f"Clicked button {index + 1}")

                    WebDriverWait(driver, 5).until(EC.staleness_of(button))
                    sleep(2)

                    try:
                        script_element = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, "//script[contains(text(), 'Answer')]"))
                        )
                        script_text = script_element.get_attribute('innerHTML')

                        match = re.search(r"Answer:\s*(\d+)", script_text)

                        if match:
                            answer = match.group(1)
                            logging.info(f"Button {index + 1} Answer is: {answer}")
                        else:
                            print("Answer not found!")

                    except StaleElementReferenceException:
                        print("Stale script element, retrying...")
                        sleep(1)  # Wait before retrying

                else:
                    logging.warning(f"No button found at index {index}")

            except Exception as e:
                logging.error(f"Error occurred on button {index + 1}: {e}")
        sleep(1)
        driver.back()
    except Exception as e:
        logging.error(f"An error occurred: {e}")


def check_boxes():
    # Check boxes
    try:
        driver.find_element(By.CSS_SELECTOR, 'a[href="/checkboxes"]').click()
        first_checkbox = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//input[1]'))
        )
        first_checkbox.click()  # it will click both check boxes
        assert first_checkbox.is_selected()
        logging.info(f"First Checkbox is selected")
        sleep(1)
        second_checkbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//input[2]'))
        )
        second_checkbox.click()  # it will un_check second box
        assert not second_checkbox.is_selected()
        logging.info('Second check box is un selected')
        first_checkbox.click()  # it will un_check second box
        second_checkbox.click()  # it will check box
        logging.info(f'second box is selected again')
        sleep(2)
        driver.back()

    except Exception as e:
        logging.error(f"An error occurred: {e}")


def context_menu():
    # Context menu
    try:
        print('Context menu')
        driver.find_element(By.CSS_SELECTOR, "a[href='/context_menu']").click()
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div#hot-spot'))
        )
        ActionChains(driver).context_click(element).perform()  # Mouse right click line
        logging.info(f"Context clicked by using action chain module")
        alert = driver.switch_to.alert
        alert_text = alert.text
        logging.info(f"Context menu alert text is : {alert_text}")
        alert.accept()
        sleep(2)
        pyautogui.click()
        sleep(1)
        driver.back()
    except Exception as e:
        logging.error(f'An error occurred : {e}')


def digest_auth():
    # digest_auth
    try:
        wait = WebDriverWait(driver, 10)
        print('Digest Authentication')
        driver.find_element(By.CSS_SELECTOR, 'a[href="/digest_auth"]').click()
        try:
            text = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div#main-message'))).text

            def is_valid_page():
                return True if "This page isn’t working" in text else False

            assert is_valid_page()
            logging.info(f"Data is not available in current page")
            sleep(1)
            driver.back()
        except:
            driver.get('https://admin:admin@the-internet.herokuapp.com/digest_auth')
            logging.warning(f"Handled page, data is available")
            driver.back()
    except Exception as e:
        logging.error(f"An error occurred : {e}")


def disappearing_elements():
    # Disappearing Elements
    try:
        print("Disappearing Elements")
        driver.find_element(By.CSS_SELECTOR, 'a[href="/disappearing_elements"]').click()

        wait = WebDriverWait(driver, 10)
        text = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.example h3')))
        assert text.is_displayed()
        logging.info(f"Text is displayed")
        try:
            all_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.example li")))

            def click_and_navigate(element_text):
                for element in all_elements:
                    if element.text == element_text:
                        element.click()
                        logging.info(f"{element_text} page is opened")
                        sleep(1)
                        driver.back()
                        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.example li')))
                        break

            pages = ['Home', 'About', 'Contact Us', 'Portfolio', 'Gallery']
            for page in pages:
                click_and_navigate(page)
            logging.info(f"All pages opened successfully")
            driver.back()
        except:
            logging.error(f"Something went wrong")

    except Exception as e:
        logging.error(f"Something went wrong {e}")


def drag_and_drop():
    try:
        print('Drag and Drop')
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/drag_and_drop"]'))).click()
        a = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#column-a')))
        b = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#column-b')))

        actions = ActionChains(driver)
        actions.drag_and_drop(a, b).perform()
        sleep(2)
        logging.info(f"A Swapped to B")
        a_column = a.text
        b_column = b.text
        try:
            all_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div#columns div')))

            def verification_drag_and_drop(column):
                for element in all_elements:
                    if element.text == column:
                        break

            columns = [a_column, b_column]
            for column in columns:
                verification_drag_and_drop(column)
            logging.info(f"Drag and drop worked successfully")

        except Exception as inner_info:
            logging.warning(f"Drag and drop checking logic as some problem {inner_info}")

        sleep(2)
        driver.back()
    except Exception as e:
        logging.error(f"An error occurred in drag and drop, {e}")


def drop_down():
    print('Drop Down')
    wait = WebDriverWait(driver,10)
    try:
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/dropdown"]'))).click()
        dropdown_elements = Select(wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'select#dropdown'))))
        for dropdown in dropdown_elements.options:
            dropdown.click()
            logging.info(f"{dropdown.text} is selected")
            sleep(2)
        sleep(2)
        driver.back()
    except Exception as e:
        logging.info(f"An Error occurred : {e}")


if __name__ == "__main__":
    try:
        a_b_testing()
        add_remove_elements()
        basic_auth()
        broken_images()
        challenging_dom()
        check_boxes()
        context_menu()
        digest_auth()
        disappearing_elements()
        drag_and_drop()
    finally:
        close_browser()
