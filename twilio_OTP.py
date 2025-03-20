from selenium import webdriver
import time
from twilio.rest import Client

# Twilio credentials
TWILIO_ACCOUNT_SID = 'your_account_sid'
TWILIO_AUTH_TOKEN = 'your_auth_token'
YOUR_PHONE_NUMBER = '9866242188'

# Initialize Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def get_latest_otp():
    # Fetch the latest SMS message sent to your phone number
    messages = client.messages.list(to=YOUR_PHONE_NUMBER, limit=1)
    for message in messages:
        return message.body  # Return the message body (OTP)

# Set up the Selenium WebDriver
driver = webdriver.Chrome()

# Navigate to the login page
driver.get("https://example.com/login")

# Enter phone number and submit
driver.find_element("id", "phone").send_keys(YOUR_PHONE_NUMBER)
driver.find_element("id", "submit").click()

# Wait for the OTP to be sent (adjust time as necessary)
time.sleep(10)  # Wait for the SMS to arrive

# Retrieve the OTP using Twilio API
otp = get_latest_otp()
print(f"Retrieved OTP: {otp}")

# Enter the OTP
driver.find_element("id", "otp").send_keys(otp)

# Continue with the login process
driver.find_element("id", "login").click()

# Close the driver
driver.quit()
