from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time


class AmazonReview:
    def __init__(self, profile_name, review_text, star_rating, link):
        self.profile_name = profile_name
        self._review_text = review_text
        self._star_rating = star_rating
        self._link = link

    def print_review(self):
        print(f"{self.profile_name} + {self.review_text} + {self._star_rating}")

    @property
    def review_text(self):
        return self._review_text

    @property
    def review_stars(self):
        return self._star_rating

    @property
    def link(self):
        return self._link


def amazon():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    # Navigate to the Amazon product page
    reviews = []
    users = []
    urls = []
    reviews_temp = []
    stars = []

    for i in range(2):
        if i == 0:
            url = "https://www.amazon.com/Bose-QuietComfort-45-Bluetooth-Canceling-Headphones/product-reviews/B098FKXT8L/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
        else:
            url = "https://www.amazon.com/Bose-QuietComfort-45-Bluetooth-Canceling-Headphones/product-reviews/B098FKXT8L/ref=cm_cr_arp_d_paging_btm_next_" + str(i + 1) + "?ie=UTF8&reviewerType=all_reviews&pageNumber=" + str(i + 1)
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
                star = j.find("i", attrs={"data-hook": "review-star-rating"}).text
                stars.append(float(str(star[0:2])))

    """debug
        for link in range(len(urls)):
            driver.get(urls[link])
            driver.implicitly_wait(5)
            time.sleep(1)
    """
    # Close the WebDriver

    # create reviews
    for i in range(len(reviews_temp)):
        reviews.append(AmazonReview(users[i], reviews_temp[i], stars[i], urls[i]))

    # debug: print(reviews[0].review_text)

    currentRating = 0.0
    adjustedRating = 0.0
    tooShort = 0
    tooFewReviews = 0
    tooPositive = 0

    # create a base rating
    for review in reviews:
        currentRating += review.review_stars
    currentRating = currentRating / float(len(reviews))

    # visit profiles
    i = len(reviews) - 1
    while i >= 0:
        # first part of logic: make sure reviews are at least 300 chars long (at least 40-80 words)
        # less length == lazy review, we want the experts
        if len(reviews[i].review_text) <= 300:
            tooShort += 1
            reviews.pop(i)
            i -= 1
            continue

        # start visiting profiles
        driver.get(reviews[i].link)
        driver.implicitly_wait(5)
        time.sleep(2)  # allow some time to load

        page_source = driver.page_source
        # parse the page source
        soup = BeautifulSoup(page_source, 'html.parser')

        # get the reviews
        review_cards = soup.find_all('div', attrs={"class": "your-content-card-column"})

        # second part of logic: check to see how many reviews they have
        # not many reviews == not credible
        if len(review_cards) <= 3:
            tooFewReviews += 1
            reviews.pop(i)
            continue

        # third part of logic: if they have a significant amount of reviews, check if they're too positive
        # all good reviews == nothing is bad == too positive of a person
        int_rating = 0
        for card in range(len(review_cards)):
            str_rating = review_cards[card].find("span", attrs={"class": "a-icon-alt"}).text
            int_rating += int(str_rating[0])

        avg_rating = int_rating / float(len(review_cards) - 1)
        if avg_rating > 4.75:
            tooPositive += 1
            reviews.pop(i)
            continue

        i -= 1

    # adjust the rating after the reviews have been removed
    for review in reviews:
        adjustedRating += review.review_stars
    adjustedRating = adjustedRating / float(len(reviews))

    # print ratings
    print("Base rating: " + str(currentRating))
    print("Too short of a review: " + str(tooShort))
    print("Not enough reviews: " + str(tooFewReviews))
    print("Too many positive reviews: " + str(tooPositive))
    print("Adjusted rating: " + str(round(adjustedRating, 2)))

    driver.quit()  # close the driver at the end


# call function
amazon()
