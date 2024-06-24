from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time


URL = "https://krisha.kz/content/analytics"


# Function to setup the WebDriver
def setup_driver(chrome_driver_path):
    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    
    # Hiding the webdriver property to avoid detection
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })
    
    return driver

# Function to scrape data
def scrape_krisha_analytics(driver, url):
    driver.get(url)
    time.sleep(3)  # Wait for the page to load
    
    # Example selectors (these need to be adapted based on the actual page structure)
    titles = driver.find_elements(By.CSS_SELECTOR, "div.analytics-item__title")
    values = driver.find_elements(By.CSS_SELECTOR, "div.analytics-item__value")
    
    data = []
    for title, value in zip(titles, values):
        data.append({
            "Title": title.text,
            "Value": value.text
        })
    
    return data

# Function to save data to CSV
def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

# Main function
def main():
    chrome_driver_path = "/path/to/your/chromedriver"  # Update this path
    URL = "https://krisha.kz/content/analytics"
    
    driver = setup_driver(chrome_driver_path)
    
    try:
        data = scrape_krisha_analytics(driver, URL)
        save_to_csv(data, "krisha_analytics.csv")
        print("Data has been successfully scraped and saved to krisha_analytics.csv")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
