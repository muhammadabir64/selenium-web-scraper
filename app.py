from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import csv

browser = webdriver.Firefox()

# Navigate to the login page and log in
browser.get('https://example-site.com/login')
email_field = browser.find_element(By.NAME, 'email')
password_field = browser.find_element(By.NAME, 'password')
email_field.send_keys('user@gmail.com')
password_field.send_keys('pass123')
password_field.send_keys(Keys.RETURN)

# Wait for a few seconds to ensure the login is complete
time.sleep(5)

# URL of the page with the table to scrape
base_url = 'https://example-site.com/data'

# Initialize a CSV file for writing
with open('data.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Column Name'])

    # Loop through pages and scrape data
    page_number = 1

    while True:
        url = f'{base_url}?page={page_number}'
        browser.get(url)

        # Locate the table with product names
        table = browser.find_element(By.ID, 'table_id')

        # Scrape data from the table and append to the CSV file
        rows = table.find_elements(By.TAG_NAME, 'tr')
        for row in rows[1:]:
            # Use find_elements to get all the table cells, and then access the third cell (index 2)
            product_name = row.find_elements(By.TAG_NAME, 'td')[2].text
            csv_writer.writerow([product_name])

        # Check if there's a "Next" button for pagination
        try:
            next_button = browser.find_element(By.LINK_TEXT, '›')
            next_button.click()
            page_number += 1
        except NoSuchElementException:
            break  # No more data to scrape

# Close the browser
browser.quit()

print('Data scraped and saved to data.csv')