from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd

# Initialize an HTML session
session = HTMLSession()

# Define the URL
url = "https://krisha.kz/content/analytics"

# Send a GET request to the URL
response = session.get(url)

# Render JavaScript
response.html.render(timeout=20)

# Parse the content with BeautifulSoup
soup = BeautifulSoup(response.html.html, 'html.parser')

# Example: Find and print all analytics items (Adjust the selectors as needed)
titles = soup.select("div.analytics-item__title")
values = soup.select("div.analytics-item__value")

data = []
for title, value in zip(titles, values):
    data.append({
        "Title": title.text.strip(),
        "Value": value.text.strip()
    })

# Save data to a CSV file
df = pd.DataFrame(data)
df.to_csv("krisha_analytics.csv", index=False)

print("Data has been successfully scraped and saved to krisha_analytics.csv")
