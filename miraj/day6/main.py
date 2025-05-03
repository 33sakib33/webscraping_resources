from bs4 import BeautifulSoup
import csv
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
driver = webdriver.Chrome(options=chrome_options)

# driver.get("https://quotes.toscrape.com/login")
# time.sleep(2)
# print("login successful")

# # Fill in login credentials (demo: admin/admin)
# driver.find_element(By.NAME, "username").send_keys("user")
# driver.find_element(By.NAME, "password").send_keys("pass")
# driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
# time.sleep(2)

url = "https://www.udemy.com/courses/development/"
driver.get(url)
time.sleep(3)

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
