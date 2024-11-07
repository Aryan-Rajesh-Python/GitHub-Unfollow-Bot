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

# Setting up logging
logging.basicConfig(level=logging.INFO)

# Avoid hardcoding credentials directly in the script
os.environ["email"] = "aryanrajesh6702@gmail.com"
os.environ["password"] = "Intrusion@7"

class GitHubBot:
    def __init__(self):
        self.start_driver()
        self.login()
        self.followers = []
        self.following = []

    def start_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(url="https://github.com/login")

    def login(self):
        email = os.environ.get("email")
        password = os.environ.get("password")
        if not email or not password:
            raise ValueError("Email and password are not set in environment variables.")
        logging.info("Logging in...")
        email_input = self.driver.find_element(By.NAME, "login")
        password_input = self.driver.find_element(By.NAME, "password")
        email_input.send_keys(email)
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)
        
        # Wait for the page to load completely after login
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Pull requests')]"))
        )
        logging.info("Login successful!")

    def wait_for_element(self, xpath, timeout=10):
        """Waits for an element to be visible and returns it."""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
            return element
        except Exception as e:
            logging.error(f"Error finding element: {e}")
            return None

    def get_users_from_page(self, account: str, page_count: int, tab: str):
        users = []
        for number in range(1, page_count + 1):
            page = f"https://github.com/{account}?page={number}&tab={tab}"
            self.driver.get(page)
            
            # Wait until the users' section is fully loaded
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[@class='Link--secondary']"))
            )
            html_content = self.driver.page_source
            soup = BeautifulSoup(html_content, 'lxml')
            users += [span.text for span in soup.find_all('span', class_='Link--secondary')]
        return users
    
    def find_followers(self):
        website = f"https://github.com/Aryan-Rajesh-Python"
        self.driver.get(website)
        html_content = self.driver.page_source
        soup = BeautifulSoup(html_content, 'lxml')
        links = soup.find_all("a", href=True)
        link = [link.text for link in links if "followers" in link['href']]
        link = re.findall(r'\d+', link[0])[0]
        page_count = int((float(link) // 50) + 1)
        self.followers = self.get_users_from_page("Aryan-Rajesh-Python", page_count, "followers")

    def find_following(self):
        website = f"https://github.com/Aryan-Rajesh-Python"
        self.driver.get(website)
        html_content = self.driver.page_source
        soup = BeautifulSoup(html_content, 'lxml')
        links = soup.find_all("a", href=True)
        link = [link.text for link in links if "following" in link['href']]
        link = re.findall(r'\d+', link[0])[0]
        page_count = int((float(link) // 50) + 1)
        self.following = self.get_users_from_page("Aryan-Rajesh-Python", page_count, "following")

    def check_accounts(self):
        self.find_followers()
        self.find_following()
        logging.info(f"Followers: {len(self.followers)}")
        logging.info(f"Following: {len(self.following)}")
        non_following = list(set(self.following) - set(self.followers))
        logging.info(f"Users not following you back: {len(non_following)}")
        logging.info(f"These are the users you can manually unfollow: {non_following}")

if __name__ == "__main__":
    github_bot = GitHubBot()
    github_bot.check_accounts()
    github_bot.driver.quit()  # Ensure the browser closes
