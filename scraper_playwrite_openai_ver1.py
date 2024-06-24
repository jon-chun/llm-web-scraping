from playwright.sync_api import sync_playwright
import pandas as pd

def scrape_krisha_analytics():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://krisha.kz/content/analytics")
        
        # Increase the timeout and wait for the necessary content to load
        page.wait_for_selector("div.analytics-item__title", timeout=60000)

        # Extract titles and values
        titles = page.query_selector_all("div.analytics-item__title")
        values = page.query_selector_all("div.analytics-item__value")

        if not titles or not values:
            print("Failed to find the expected elements on the page.")
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
