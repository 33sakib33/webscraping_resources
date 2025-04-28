import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

def scrape_quotes(base_url):
    all_quotes = []
    url = base_url
    
    while url:
        print(f"Scraping page: {url}")
        response = requests.get(url)
        
        if response.status_code != 200:
            print(f"Failed to retrieve page: {url}")
            break
            
        soup = BeautifulSoup(response.text, 'html.parser')
        quotes = soup.find_all('div', class_='quote')
        
        for quote in quotes:
            # Extract quote text
            text = quote.find('span', class_='text').text.strip('“”')
            
            # Extract author information
            author = quote.find('small', class_='author').text
            about_link = quote.find('a', href=True)['href']
            author_url = urljoin(base_url, about_link)
            
            # Extract tags
            tags = [tag.text for tag in quote.find_all('a', class_='tag')]
            meta_keywords = quote.find('meta', class_='keywords')['content'] if quote.find('meta', class_='keywords') else ''
            
            # Store all data
            quote_data = {
                'text': text,
                'author': author,
                'author_url': author_url,
                'tags': tags,
                'meta_keywords': meta_keywords,
                'page_url': url
            }
            all_quotes.append(quote_data)
        
        # Check for next page
        next_button = soup.find('li', class_='next')
        if next_button:
            next_page = next_button.find('a')['href']
            url = urljoin(base_url, next_page)
        else:
            url = None
    
    return all_quotes

def save_to_csv(quotes, filename='quotes_data.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=[
            'text', 'author', 'author_url', 'tags', 'meta_keywords', 'page_url'
        ])
        writer.writeheader()
        writer.writerows(quotes)

def main():
    base_url = "https://quotes.toscrape.com/"
    quotes = scrape_quotes(base_url)
    
    print(f"\nScraped {len(quotes)} quotes in total.")
    
    # Save to CSV
    save_to_csv(quotes)
    print("Data saved to quotes_data.csv")
    
    # Print sample data
    print("\nSample quote data:")
    print(quotes[0])

if __name__ == "__main__":
    main()
