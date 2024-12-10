from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import logging
import os
from bs4 import BeautifulSoup
import re
import math

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("github_bot.log"),  # Log to file
        logging.StreamHandler()                # Log to console
    ]
)

os.environ["email"] = "aryanrajesh6702@gmail.com"
os.environ["password"] = "Intrusion@7"

class GitHubBot:
    def __init__(self):
        self.start_driver()
        self.login()
        self.followers = []
        self.following = []

    def start_driver(self):
        """Starts the WebDriver with optimized settings."""
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--headless=new")  # Run browser in headless mode
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_page_load_timeout(15)
        self.driver.get("https://github.com/login")

    def login(self):
        """Logs into GitHub."""
        logging.info("Logging in...")
        try:
            email = os.getenv("email")
            password = os.getenv("password")
            if not email or not password:
                raise ValueError("Email or password not set in environment variables.")
            
            email_input = self.driver.find_element(By.NAME, "login")
            password_input = self.driver.find_element(By.NAME, "password")
            email_input.send_keys(email)
            password_input.send_keys(password)
            password_input.send_keys(Keys.ENTER)

            # Wait for the main page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Pull requests')]"))
            )
            logging.info("Login successful!")
        except Exception as e:
            logging.error(f"Login failed: {e}")
            self.driver.quit()

    def fetch_user_list(self, account, page_count, tab):
        """Fetches users from the specified tab."""
        users = []
        for page in range(1, page_count + 1):
            try:
                logging.info(f"Fetching {tab} data: Page {page}/{page_count}")
                self.driver.get(f"https://github.com/{account}?page={page}&tab={tab}")
                
                # Wait until the user list is loaded
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//span[@class='Link--secondary']"))
                )

                # Parse the page content
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                users_on_page = [span.text.strip() for span in soup.find_all('span', class_='Link--secondary')]
                users.extend(users_on_page)
            except Exception as e:
                logging.warning(f"Failed to fetch {tab} data from page {page}: {e}")
                continue
            finally:
                time.sleep(1)  # Small delay to avoid rate-limiting
        return users

    def get_followers_following(self):
        """Fetches followers and following lists."""
        try:
            self.followers = self.fetch_user_list("Aryan-Rajesh-Python", 2, "followers")
            self.following = self.fetch_user_list("Aryan-Rajesh-Python", 3, "following")
            logging.info(f"Followers fetched: {len(self.followers)}")
            logging.info(f"Following fetched: {len(self.following)}")
        except Exception as e:
            logging.error(f"Error fetching followers/following: {e}")

    def check_non_following(self):
        """Identifies users not following back."""
        self.get_followers_following()
        non_following = list(set(self.following) - set(self.followers))
        logging.info(f"Users not following you back ({len(non_following)}): {', '.join(non_following)}")
        print(f"\nUsers not following you back: {len(non_following)}")
        print(f"Manual unfollow recommended for:\n{', '.join(non_following)}\n")

if __name__ == "__main__":
    try:
        bot = GitHubBot()
        bot.check_non_following()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        if hasattr(bot, 'driver'):
            bot.driver.quit()
