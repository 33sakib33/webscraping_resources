from bs4 import BeautifulSoup
import csv
from selenium import webdriver
import time


driver = webdriver.Chrome()

url = "https://quotes.toscrape.com/scroll"
driver.get(url)
time.sleep(3)

soup = BeautifulSoup(driver.page_source, "html.parser")

quotes = soup.find_all("div", class_="quote")

with open('life_quotes_day3.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['sl', 'quote', 'by whom', 'tags'])

    for idx, quote in enumerate(quotes[:10], start=1):
        text = quote.find("span", class_="text").get_text(strip=True)
        author = quote.find("small", class_="author").get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in quote.find_all("a", class_="tag")]
        tags_string = ", ".join(tags)

        writer.writerow([idx, text, author, tags_string])

print("Done")


# requests + BeautifulSoup = only for static HTML pages.
# Selenium = for dynamic JavaScript-powered websites like /scroll.
