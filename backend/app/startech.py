from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os

def scrape_startech(query):
    # Initialize the Selenium WebDriver
    options = Options()
    options.add_argument("--headless")
    # Cache browser data for faster scraping
    datadir = os.environ['HOME'] + "/BestDealData/Startech"
    options.add_argument(f"user-data-dir={datadir}")
    options.binary_location = os.environ['BROWSER']
    driver = webdriver.Chrome(options=options)

    # Encode the query for the URL
    encoded_query = query.replace(" ", "%20")

    # Send a request to the search page
    driver.get(f"https://www.startech.com.bd/product/search?search={encoded_query}")

    # Create a list to store search results
    search_results = []
    logo = 'startech.png'

    # Wait for the page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div[2]/div')))

    # Now, you can collect all the search results
    result_elements = driver.find_elements(By.XPATH, '//*[@id="content"]/div[2]/div')
    total_items = len(result_elements)

    for item_id in range(1, total_items):
        try:
            title = driver.find_element(By.XPATH, f'//*[@id="content"]/div[2]/div[{item_id}]/div/div[3]/h4/a')
            price = driver.find_element(By.XPATH, f'//*[@id="content"]/div[2]/div[{item_id}]/div/div[3]/div[2]/span[1]')
            image = driver.find_element(By.XPATH, f'//*[@id="content"]/div[2]/div[{item_id}]/div/div[2]/a/img').get_attribute('src')
            link = title.get_attribute('href')
            
            if (price.text == "TBA" or price.text == "Out Of Stock" or price.text == "Up Coming"):
                continue
            search_results.append({
                "title": title.text,
                "price": price.text,
                "image": image,
                "link": link,
                "logo": logo,
            })
        except Exception as e:
            if 'DEBUG' in os.environ:
                print(f"[Startech search] Exception: {e}")
            pass

    # After scraping, close the browser window
    driver.quit()

    return search_results
