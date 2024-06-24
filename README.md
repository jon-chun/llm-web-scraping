
# Krisha.kz Analytics Scraper

This repository contains a Python script to scrape analytics data from [Krisha.kz](https://krisha.kz/content/analytics) and save it into a CSV file.

## Table of Contents
- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [Chrome and ChromeDriver Setup](#chrome-and-chromedriver-setup)
  - [Check Versions](#check-versions)
  - [Download and Install ChromeDriver](#download-and-install-chromedriver)
  - [Install Older Chrome Versions](#install-older-chrome-versions)

## Requirements
- Python 3.6+
- Google Chrome browser
- ChromeDriver

## Setup
1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/krisha-analytics-scraper.git
    cd krisha-analytics-scraper
    ```

2. **Create a virtual environment** (optional but recommended):
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required packages**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Download ChromeDriver** and place it in a known location. Ensure the version matches your Chrome browser version (see details below).

5. **Update the `chrome_driver_path`** in `scrape_krisha.py`:
    ```python
    chrome_driver_path = "/path/to/your/chromedriver"
    ```

## Usage
Run the scraper script:
```sh
python scrape_krisha.py
```
The data will be saved to `krisha_analytics.csv` in the current directory.

## Chrome and ChromeDriver Setup

### Check Versions
1. **Check Chrome Version**:
   - Open Google Chrome and navigate to `chrome://version`.
   - Note the version number (e.g., `91.0.4472.124`).

2. **Check ChromeDriver Version**:
   - Visit the [ChromeDriver download page](https://sites.google.com/chromium.org/driver/downloads) and ensure you download the version that matches your Chrome browser version.

### Download and Install ChromeDriver
1. Download the appropriate version from the [ChromeDriver download page](https://sites.google.com/chromium.org/driver/downloads).
2. Place the ChromeDriver executable in a known location and update the `chrome_driver_path` in `scrape_krisha.py`.

### Install Older Chrome Versions
If needed, you can roll back or install older versions of Chrome:

- **Windows**:
  - Uninstall current Chrome version.
  - Download older version from [Chrome for Windows](https://www.slimjet.com/chrome/google-chrome-old-version.php).

- **Mac**:
  - Use a package manager like `brew` to manage Chrome versions.
  - Commands to uninstall and install specific versions can be found on [Homebrew's documentation](https://formulae.brew.sh/cask/google-chrome).

- **Linux**:
  - Use your distribution's package manager to manage Chrome versions.
  - Specific commands will vary by distribution (e.g., `apt`, `yum`, `dnf`).

## Troubleshooting
- Ensure ChromeDriver and Chrome versions match.
- Check permissions of the ChromeDriver executable.
- Refer to [ChromeDriver documentation](https://chromedriver.chromium.org/) for more details.

## Additional Notes
- For dynamic content, consider using browser automation tools like Selenium or Puppeteer.
- Review and comply with the website's `robots.txt` and terms of service when scraping data.
