from bs4 import BeautifulSoup
import csv
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://quotes.toscrape.com/login")
time.sleep(2)
print("login successful")

# Fill in login credentials (demo: admin/admin)
driver.find_element(By.NAME, "username").send_keys("user")
driver.find_element(By.NAME, "password").send_keys("pass")
driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
time.sleep(2)

url = "https://quotes.toscrape.com/scroll"
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

quotes = soup.find_all("div", class_="quote")

life_quotes = []

for quote in quotes:
    tags = [tag.get_text(strip=True) for tag in quote.find_all("a", class_="tag")]
    if "life" in tags:
        life_quotes.append(quote)

with open('life_quotes.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['sl', 'quote', 'by whom', 'tags'])

    for idx, quote in enumerate(life_quotes, start=1):
        text = quote.find("span", class_="text").get_text(strip=True)
        author = quote.find("small", class_="author").get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in quote.find_all("a", class_="tag")]
        tags_string = ", ".join(tags)

        writer.writerow([idx, text, author, tags_string])

print("Done")
