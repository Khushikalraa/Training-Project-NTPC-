from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time
from datetime import datetime

# Define paths to the chromedriver executable
path = '/Users/salonikalra/Desktop/NTPC /chromedriver'

chrome_options = Options()
# Comment out headless mode for troubleshooting
# chrome_options.add_argument('--headless')

chrome_service = Service(executable_path=path)

weather_data = []
nrldc_data = []

# Define the start time
start_time = datetime.strptime('2024-07-05 18:28:50', '%Y-%m-%d %H:%M:%S')

# Wait until the start time
while datetime.now() < start_time:
    time_to_wait = (start_time - datetime.now()).total_seconds()
    print(f"Waiting for {time_to_wait} seconds until the start time.")
    time.sleep(min(time_to_wait, 2))  # Wait for the lesser of the time to wait or 2 seconds

try:
    # Initialize the WebDriver outside the loop
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    print("Chrome browser opened successfully.")

    while True:
        # Scrape weather data
        driver.get("https://www.accuweather.com/en/in/noida/3146227/weather-forecast/3146227")
        time.sleep(5)  # Wait for the page to load

        try:
            # Extract temperature
            temp_element = driver.find_element(By.CSS_SELECTOR, "div.cur-con-weather-card__body .temp")
            temperature = temp_element.text.split("°")[0]

            # Get current time
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Append weather data
            weather_data.append([temperature, current_time])

            # Convert to DataFrame and save to CSV
            weather_df = pd.DataFrame(weather_data, columns=["Temperature", "Time"])
            weather_df.to_csv("Weather3.csv", index=False)

            print(f"Weather data at {current_time}: {temperature}°C")

        except Exception as e:
            print(f"Error extracting temperature: {e}")

        # Scrape NR Grid frequency data
        driver.get("https://nrldc.in")
        time.sleep(5)  # Wait for the page to load (adjust as needed)

        try:
            # Locate the specific span containing the frequency value
            frequency_span = driver.find_element(By.CSS_SELECTOR, ".wrap .home-welcome.widget-area .widget_black_studio_tinymce .widget-wrap .textwidget p:nth-of-type(2) span")

            # Extract and clean the frequency text
            frequency_text = frequency_span.text.strip()

            # Get current time
            current_time = datetime.now().strftime("%H:%M")

            # Append NR Grid frequency data
            nrldc_data.append([frequency_text, current_time])

            # Convert to DataFrame and save to CSV
            nrldc_df = pd.DataFrame(nrldc_data, columns=["Frequency", "Time"])
            nrldc_df.to_csv("nrldc_data3.csv", index=False)

            print(f"NR Grid data at {current_time}: Frequency {frequency_text}")

        except Exception as e:
            print(f"Error extracting frequency: {e}")

        # Wait for 2 minutes before the next scrape
        time.sleep(120)

except KeyboardInterrupt:
    print("Scraping stopped by user.")

finally:
    driver.quit()
    print("Data has been scraped and saved to Weather.csv and nrldc_data.csv")
