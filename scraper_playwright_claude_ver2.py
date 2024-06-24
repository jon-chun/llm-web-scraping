from playwright.sync_api import sync_playwright
import pandas as pd
import time
import re
import json

def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

def extract_number(text):
    match = re.search(r'([\d\s]+(?:,\d+)?)', text)
    if match:
        return match.group(1).replace(' ', '')
    return ''

def scrape_krisha_analytics():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        try:
            page.goto("https://krisha.kz/content/analytics", timeout=60000)
        except Exception as e:
            print(f"Error loading page: {e}")
            browser.close()
            return

        try:
            page.wait_for_selector("div.analytics-item__title", timeout=60000)
        except Exception as e:
            print(f"Error waiting for selector: {e}")
            print("Current page content:")
            print(page.content())
            browser.close()
            return

        time.sleep(5)

        # Extract general analytics data
        analytics_data = []
        analytics_items = page.query_selector_all("div.analytics-item")
        for item in analytics_items:
            title = item.query_selector("div.analytics-item__title")
            value = item.query_selector("div.analytics-item__value")
            if title and value:
                analytics_data.append({
                    "Type": "General",
                    "Title": clean_text(title.inner_text()),
                    "Value": clean_text(value.inner_text())
                })

        # Extract table data
        table_data = []
        tables = page.query_selector_all("table")
        for table in tables:
            headers = [clean_text(th.inner_text()) for th in table.query_selector_all("th")]
            rows = table.query_selector_all("tr")
            for row in rows[1:]:  # Skip header row
                cells = row.query_selector_all("td")
                row_data = [clean_text(cell.inner_text()) for cell in cells]
                if len(row_data) == len(headers):
                    table_data.append(dict(zip(headers, row_data)))

        # Extract chart data
        chart_data = []
        charts = page.query_selector_all("div.chart-wrapper")
        for chart in charts:
            chart_title = clean_text(chart.query_selector("h3").inner_text())
            bars = chart.query_selector_all("div.chart-bar")
            for bar in bars:
                # Hover over the bar to trigger the popup
                bar.hover()
                time.sleep(0.5)  # Wait for popup to appear
                
                popup = page.query_selector("div.chart-tooltip")
                if popup:
                    popup_text = clean_text(popup.inner_text())
                    # Extract data from popup text
                    date_match = re.search(r'(\w+\s+\d{4})', popup_text)
                    value_match = re.search(r'([\d\s]+(?:,\d+)?)\s+тг', popup_text)
                    
                    date = date_match.group(1) if date_match else ''
                    value = extract_number(value_match.group(1)) if value_match else ''
                    
                    chart_data.append({
                        "Chart": chart_title,
                        "Date": date,
                        "Value": value
                    })

        # Combine all data
        all_data = analytics_data + table_data + chart_data

        # Save data to a CSV file
        df = pd.DataFrame(all_data)
        df.to_csv("krisha_analytics_full.csv", index=False, encoding='utf-8-sig')

        print("Data has been successfully scraped and saved to krisha_analytics_full.csv")
        
        browser.close()

if __name__ == "__main__":
    scrape_krisha_analytics()