import requests
from bs4 import BeautifulSoup

# URL of the quote site
url = "http://quotes.toscrape.com/"

# Send request
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Find all quotes on the page
quotes = soup.find_all("div", class_="quote")

# Loop through each quote and print
for quote in quotes:
    text = quote.find("span", class_="text").get_text()
    author = quote.find("small", class_="author").get_text()
    tags = [tag.get_text() for tag in quote.find_all("a", class_="tag")]

    print(f"Quote: {text}")
    print(f"Author: {author}")
    print(f"Tags: {', '.join(tags)}")
    print("-" * 50)
