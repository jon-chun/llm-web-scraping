from playwright.sync_api import sync_playwright
import pandas as pd
import time
import re

def extract_chart_data():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        try:
            print("Navigating to the page...")
            page.goto("https://krisha.kz/content/analytics", timeout=120000)
        except Exception as e:
            print(f"Error loading page: {e}")
            browser.close()
            return

        try:
            print("Waiting for chart to load...")
            page.wait_for_selector(".chart-wrapper", timeout=120000)
        except Exception as e:
            print(f"Error waiting for chart: {e}")
            browser.close()
            return

        print("Chart found. Extracting data...")

        # Extract chart data
        chart_data = []
        bars = page.query_selector_all(".chart-bar")
        
        for bar in bars:
            bar.hover()
            time.sleep(0.5)  # Wait for tooltip to appear
            
            tooltip = page.query_selector(".chart-tooltip")
            if tooltip:
                tooltip_text = tooltip.inner_text()
                date_match = re.search(r'(\w+\s+\d{4})', tooltip_text)
                value_match = re.search(r'([\d\s]+(?:,\d+)?)\s+тг', tooltip_text)
                
                date = date_match.group(1) if date_match else ''
                value = value_match.group(1).replace(' ', '') if value_match else ''
                
                chart_data.append({
                    "Date": date,
                    "Value": value
                })

        # Save data to CSV
        df = pd.DataFrame(chart_data)
        output_file = "krisha_chart_data.csv"
        df.to_csv(output_file, index=False)

        print(f"Data has been successfully scraped and saved to {output_file}")
        
        browser.close()

if __name__ == "__main__":
    extract_chart_data()