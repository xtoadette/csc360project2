from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selectorlib import Extractor
import json
import time


def amazon():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    # Navigate to the Amazon product page
    url = "https://www.amazon.com/Bose-QuietComfort-Bluetooth-Cancelling-Headphones/product-reviews/B09NCHTW21/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
    driver.get(url)
    driver.implicitly_wait(5)

    reviewList = []
    userURL = []
    users = {}

    time.sleep(3) # allow time to load

    # Extract the page source after scrolling
    page_source = driver.page_source

    # parse the page source
    soup = BeautifulSoup(page_source, 'html.parser')

    # Extract and print the reviews
    reviews = soup.find_all('div', attrs={"data-hook": "review"})
    profile_links = soup.find_all('a', attrs={"class": "a-profile"})
    real_links = [profile_link["href"] for profile_link in profile_links]
    linkcounter = 0
    for i in reviews:
        reviewList.append((i.find("span", attrs={"data-hook": "review-body"})).text)
        users[(i.find("span", attrs={"class": "a-profile-name"})).text] = reviewList[linkcounter]
        linkcounter += 1

    # Close the WebDriver
    driver.quit()

    for review in reviewList:
        print(review)

    for user in users:
        print(user)


# call function
amazon()
