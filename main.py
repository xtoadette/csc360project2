from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time


class AmazonReview:
    def __init__(self, profile_name, review_text):
        self.profile_name = profile_name
        self._review_text = review_text

    def print_review(self):
        print(f"{self.profile_name} + {self.review_text}")

    @property
    def review_text(self):
        return self._review_text


def amazon():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    # Navigate to the Amazon product page
    reviews = []
    users = []
    urls = []
    reviews_temp = []

    for i in range(1):
        if i == 0:
            url = "https://www.amazon.com/Bose-QuietComfort-45-Bluetooth-Canceling-Headphones/product-reviews/B098FKXT8L/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
        else:
            url = "https://www.amazon.com/Bose-QuietComfort-45-Bluetooth-Canceling-Headphones/product-reviews/B098FKXT8L/ref=cm_cr_arp_d_paging_btm_next_" + str(i - 1) + "?ie=UTF8&reviewerType=all_reviews&pageNumber=" + str(i-1)
        driver.get(url)
        driver.implicitly_wait(5)
        time.sleep(3)  # allow time to load

        # Extract the page source after scrolling
        page_source = driver.page_source

        # parse the page source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Extract and print the reviews
        scraped_reviews = soup.find_all('div', attrs={"class": "a-section celwidget"})

        # get profile links, review text, and user names
        for j in scraped_reviews:
            profile_link = j.find_next('a', attrs={"class": "a-profile"})
            if profile_link:
                urls.append("https://www.amazon.com" + profile_link.get("href"))
                reviews_temp.append((j.find("span", attrs={"data-hook": "review-body"})).text)
                users.append(j.find("span", attrs={"class": "a-profile-name"}).text)

    """debug
        for link in range(len(urls)):
            driver.get(urls[link])
            driver.implicitly_wait(5)
            time.sleep(1)
    """
    # Close the WebDriver
    driver.quit()

    # create reviews
    for j in range(len(reviews_temp)):
        reviews.append(AmazonReview(users[j], reviews_temp[j]))

    # debug: print(reviews[0].review_text)

    # first part of logic: make sure reviews are at least 300 chars long (at least 40-80 words)
    for j in range(len(reviews)):
        if len(reviews[j].review_text) <= 300:
            reviews.pop(j)

    for review in reviews:
        review.print_review()


# call function
amazon()
