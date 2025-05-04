from bs4 import BeautifulSoup
import csv
from selenium import webdriver
import time
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
driver = webdriver.Chrome(options=chrome_options)

url = "https://www.udemy.com/courses/development/"
driver.get(url)
time.sleep(3)

def click_next_until_gone(driver):
    while True:
        try:
            # Wait for the button to be visible and clickable
            next_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.ud-carousel-pager-button-next'))
            )
            next_button.click()
            time.sleep(1.5)  # Allow content to load
        except (TimeoutException, NoSuchElementException, ElementNotInteractableException):
            print("No more Next button found. Exiting scroll.")
            break

click_next_until_gone(driver)

def scroll_until_end():
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # wait for new quotes to load

        # Calculate new scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            # No new content loaded
            break
        last_height = new_height

scroll_until_end()

soup = BeautifulSoup(driver.page_source, "html.parser")


course_cards = soup.find_all("div", class_="course-unit_course-card__5kj2f")
print(course_cards)


courses = []
for card in course_cards:
    title_tag = card.find("h3", class_="course-card-title_course-title___sH9w")
    title = title_tag.get_text(strip=True) if title_tag else "No title"

    ribbons_container = card.find("div", class_="course-card-ribbons_course-ribbons__ZLs29")
    is_bestseller = "Bestseller" in ribbons_container.text if ribbons_container else False

    if is_bestseller:
        courses.append([title, "Yes" if is_bestseller else "No"])

with open('scrapped.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Course Title", "Bestseller"])
    writer.writerows(courses)

driver.quit()

print("Done")
