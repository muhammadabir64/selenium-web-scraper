from selenium import webdriver
from selenium.webdriver.common.by import By
import csv

def scrape_product_data(product):
    title = product.find_element(By.CSS_SELECTOR, '.woocommerce-LoopProduct-link h2').text
    
    # Initialize sale price and regular price as empty strings
    sale_price = ""
    regular_price = ""
    
    # Try to find the sale price element
    try:
        sale_price_element = product.find_element(By.CSS_SELECTOR, '.price ins .woocommerce-Price-amount')
        sale_price = sale_price_element.text.split()[1].replace(',', '')  # Remove commas from the amount
        sale_price = sale_price.split('.')[0]  # Keep only the integer part
    except:
        pass
    
    # Try to find the regular price element
    try:
        regular_price_element = product.find_element(By.CSS_SELECTOR, '.price del .woocommerce-Price-amount')
        regular_price = regular_price_element.text.split()[1].replace(',', '')  # Remove commas from the amount
        regular_price = regular_price.split('.')[0]  # Keep only the integer part
    except:
        pass
    
    return {'title': title, 'sale_price': sale_price, 'regular_price': regular_price}

def scrape_all_pages(url, max_page_number):
    browser = webdriver.Firefox()
    browser.get(url)

    # Initialize a CSV file for writing
    with open('product_data.csv', 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=['title', 'sale_price', 'regular_price'])
        csv_writer.writeheader()

        # Loop through pages and scrape data
        for page_number in range(1, max_page_number + 1):
            page_url = f'{url}/page/{page_number}'
            browser.get(page_url)
            print("Scraping page " + str(page_number) + " - " + page_url)

            # Locate the container with products
            products_container = browser.find_element(By.CSS_SELECTOR, 'ul.products')

            # Scrape data from products and append to the CSV file
            products = products_container.find_elements(By.CSS_SELECTOR, 'li.product')
            for product in products:
                product_data = scrape_product_data(product)
                csv_writer.writerow(product_data)

            # Check if there are no more products on the next page
            if not products:
                break

    # Close the browser
    browser.quit()

if __name__ == "__main__":
    scrape_all_pages("https://aroz.com.bd/gadget", 1)
