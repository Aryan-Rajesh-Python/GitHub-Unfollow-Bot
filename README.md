# GitHub Unfollow Bot

This is a Python bot that automates the process of checking users you are following on GitHub and identifies those who are not following you back. You can manually unfollow these users after the script displays the list.

## Features
- Login to GitHub account using Selenium and web scraping with BeautifulSoup.
- Retrieves a list of followers and users you are following.
- Compares the lists and identifies users who are not following you back.
- Outputs a list of users you can manually unfollow.

## Prerequisites
To use this bot, you need:
- Python 3.x
- Google Chrome or a compatible browser
- ChromeDriver installed and available in your system's PATH

## Steps to run:

   ```bash
   git clone https://github.com/Aryan-Rajesh-Python/GitHub-Unfollow-Bot.git
   cd GitHub-Unfollow-Bot
   python bot.py
