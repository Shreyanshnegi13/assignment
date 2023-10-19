import requests
from bs4 import BeautifulSoup
import csv
import time
import random


# Define a list of proxy IP addresses (replace with your proxy list)
proxies = {
    "http": "http://your-proxy-ip:your-proxy-port",
    "https": "https://your-proxy-ip:your-proxy-port"
}

# Define the URL template for search results
base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{}"

# Define headers with a random user agent
user_agents = [
    "User-Agent 1",
    "User-Agent 2",
    # Add more user agents here
]

# List to store product data
product_data = []

# Define the number of pages you want to scrape (e.g., 20 for 200 products)
num_pages_part1 = 20

for page in range(1, num_pages_part1 + 1):
    url = base_url.format(page)

    headers = {"User-Agent": random.choice(user_agents)}

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            products = soup.find_all('div', {'data-component-type': 's-search-result'})

            for product in products:
                product_url = "https://www.amazon.in" + product.find('a', {'class': 'a-link-normal'})['href']
                product_name = product.find('span', {'class': 'a-text-normal'}).text
                product_price = product.find('span', {'class': 'a-price-whole'}).text
                product_rating = product.find('span', {'class': 'a-icon-alt'}).text
                product_reviews = product.find('span', {'class': 'a-size-base'}).text

                product_data.append([product_url, product_name, product_price, product_rating, product_reviews])
                
                print("Product : ",product_url, product_name, product_price, product_rating, product_reviews)
                time.sleep(random.uniform(1.0, 2.0))  # Add a random delay to avoid detection

        else:
            print(f"Failed to fetch page {page}. Status code: {response.status_code}")

    except Exception as e:
        print(f"Failed to fetch page {page}: {str(e)}")

# Rest of the code for Part 2 and exporting data remains the same

# Part 2: Scrape additional details for each product URL

# Define the number of product URLs to scrape (around 200)
num_product_urls_part2 = 200
product_data_part2 = []

# Function to scrape product details
def scrape_product_details(product_url):
    product_response = requests.get(product_url)
    if product_response.status_code == 200:
        product_soup = BeautifulSoup(product_response.content, 'html.parser')
        product_name = product_soup.find('span', {'id': 'productTitle'}).get_text(strip=True)
        product_asin = product_url.split('/')[-1].split('?')[0]
        product_description = product_soup.find('div', {'id': 'productDescription'}).get_text(strip=True)
        product_manufacturer = product_soup.find('a', {'id': 'bylineInfo'}).get_text(strip=True)
        return [product_url, product_name, product_asin, product_description, product_manufacturer]
    return None

# Iterate through the collected product URLs
for product_url in product_data[:num_product_urls_part2]:
    product_info = scrape_product_details(product_url[0])
    if product_info:
        product_data_part2.append(product_info)
    
    time.sleep(1)  # Add a delay to avoid overloading the server

# Export the collected data to a CSV file
with open('amazon_products_combined.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    # Header for Part 1
    csv_writer.writerow(['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews'])
    csv_writer.writerows(product_data)
    # Header for Part 2
    csv_writer.writerow(['Product URL', 'Product Name', 'ASIN', 'Product Description', 'Manufacturer'])
    csv_writer.writerows(product_data_part2)
