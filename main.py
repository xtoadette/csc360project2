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

class AmazonReview:
    def __init__(self, profile_name, review_text):
        self.profile_name = profile_name
        self.review_text = review_text

    def print_review(self):
        print(f"{self.profile_name} + {self.review_text}")

def amazon():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    # Navigate to the Amazon product page
    url = "https://www.amazon.com/Bose-QuietComfort-45-Bluetooth-Canceling-Headphones/product-reviews/B098FKXT8L/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
    driver.get(url)
    driver.implicitly_wait(5)

    reviews = []
    users = []
    reviews_temp = []

    time.sleep(3) # allow time to load

    # Extract the page source after scrolling
    page_source = driver.page_source

    # parse the page source
    soup = BeautifulSoup(page_source, 'html.parser')

    # Extract and print the reviews
    scraped_reviews = soup.find_all('div', attrs={"data-hook": "review"})
    profile_links = soup.find_all('a', attrs={"class": "a-profile"})
    real_links = [profile_link["href"] for profile_link in profile_links]
    print(type(real_links))
    for i in scraped_reviews:
        reviews_temp.append((i.find("span", attrs={"data-hook": "review-body"})).text)
        users.append(i.find("span", attrs={"class": "a-profile-name"}).text)

    for link in range(len(real_links)):
        driver.get("https://amazon.com" + real_links[link])
        driver.implicitly_wait(5)

    # Close the WebDriver
    driver.quit()

    # create reviews
    for i in range(len(reviews_temp)):
        reviews.append(AmazonReview(users[i], reviews_temp[i]))

    for review in reviews:
        review.print_review()


# call function
amazon()
