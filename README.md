# Automated Web Scraping using Selenium
This Python script demonstrates how to automate web scraping using Selenium, specifically for a website that requires logging in to access data from a table and saving it to a CSV file.

## Requirements:
- Python (with Selenium library installed)
- Web browser (e.g., Firefox)

##Code Overview:
1. **Importing Necessary Libraries**
- The script imports required modules from Selenium (webdriver, By, Keys, NoSuchElementException) along with time and csv modules.

2. **Setting up WebDriver**
```python
browser = webdriver.Firefox()
```
Initializes a Firefox WebDriver instance.

3. Logging into a Website
Navigates to the login page and logs in using provided credentials.

4. Scraping Data from Table
Defines the base URL for the page with the table to scrape.
Initializes a CSV file for writing.
Loops through each page, locating the table, scraping data (specifically the product names), and appending it to a CSV file.
Handles pagination by checking for a "Next" button, clicking it to move to the next page, and repeating the scraping process until there is no more data to scrape.
5. Saving Data
Closes the browser after the scraping process is completed and displays a message confirming the successful scraping and saving of data to data.csv.

Usage:
Replace 'https://example-site.com/login' with the actual login URL and provide valid credentials.
Replace 'https://example-site.com/data' with the URL containing the table to scrape and update the table identifier (table_id) if necessary.
Run the script to automate the scraping process.

### full code
```python
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
```
