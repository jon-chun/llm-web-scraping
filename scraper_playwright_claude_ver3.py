from playwright.sync_api import sync_playwright
import pandas as pd
import time
import os

def scrape_krisha_analytics():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        try:
            print("Navigating to the page...")
            page.goto("https://krisha.kz/content/analytics", timeout=120000)  # Increase timeout to 2 minutes
        except Exception as e:
            print(f"Error loading page: {e}")
            print("Current page content:")
            print(page.content())
            page.screenshot(path="error_screenshot.png")
            browser.close()
            return

        try:
            print("Waiting for selector...")
            page.wait_for_selector("div.analytics-item__title", timeout=120000)  # Increase timeout to 2 minutes
        except Exception as e:
            print(f"Error waiting for selector: {e}")
            print("Current page content:")
            print(page.content())
            page.screenshot(path="error_screenshot.png")
            browser.close()
            return

        print("Selector found. Proceeding with data extraction...")

        # Extract titles and values
        titles = page.query_selector_all("div.analytics-item__title")
        values = page.query_selector_all("div.analytics-item__value")

        if not titles or not values:
            print("No data found. Selectors might have changed.")
            print("Current page content:")
            print(page.content())
            page.screenshot(path="error_screenshot.png")
            browser.close()
            return

        data = []
        for title, value in zip(titles, values):
            data.append({
                "Title": title.inner_text().strip(),
                "Value": value.inner_text().strip()
            })

        # Save data to a CSV file
        df = pd.DataFrame(data)
        output_file = "krisha_analytics.csv"
        df.to_csv(output_file, index=False, encoding='utf-8-sig')

        print(f"Data has been successfully scraped and saved to {output_file}")
        print(f"Current working directory: {os.getcwd()}")
        
        browser.close()

if __name__ == "__main__":
    scrape_krisha_analytics()