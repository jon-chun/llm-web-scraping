from playwright.sync_api import sync_playwright
import pandas as pd
import time

def scrape_krisha_analytics():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Change to headless=False for debugging
        page = browser.new_page()
        
        try:
            page.goto("https://krisha.kz/content/analytics", timeout=60000)  # Increase timeout to 60 seconds
        except Exception as e:
            print(f"Error loading page: {e}")
            browser.close()
            return

        # Wait for the necessary content to load with a longer timeout
        try:
            page.wait_for_selector("div.analytics-item__title", timeout=60000)
        except Exception as e:
            print(f"Error waiting for selector: {e}")
            print("Current page content:")
            print(page.content())
            browser.close()
            return

        # Add a small delay to ensure everything is loaded
        time.sleep(5)

        # Extract titles and values
        titles = page.query_selector_all("div.analytics-item__title")
        values = page.query_selector_all("div.analytics-item__value")

        if not titles or not values:
            print("No data found. Selectors might have changed.")
            print("Current page content:")
            print(page.content())
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
        df.to_csv("krisha_analytics.csv", index=False)

        print("Data has been successfully scraped and saved to krisha_analytics.csv")
        
        browser.close()

if __name__ == "__main__":
    scrape_krisha_analytics()