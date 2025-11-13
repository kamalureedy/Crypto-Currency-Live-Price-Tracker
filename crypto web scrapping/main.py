import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

website = 'https://www.coingecko.com/'
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(website)

print("Rank | Name | Price | 1h | 24h | 7d | Market Cap")

# File path for CSV (auto-created in same folder as script)
filename = "crypto_data.csv"

# Create an empty list to store data before writing
all_data = []

try:
    while True:
        time.sleep(10)  # wait for data to load
        try:
            tbody = driver.find_element(By.CSS_SELECTOR,
                "body > div.container > main > div > div.gecko-sticky-table-wrapper > table > tbody")

            print("\n" + "-" * 80)
            print("Updated:", time.strftime("%H:%M:%S"))
            print("Rank | Name | Price | 1h | 24h | 7d | Market Cap")

            for i in range(1, 11):
                row = tbody.find_element(By.CSS_SELECTOR, f"tr:nth-child({i})")
                cols = [td.text for td in row.find_elements(By.TAG_NAME, "td")]

                rank = cols[1]
                name = cols[2].split('\n')[0]
                price = cols[4]
                h1 = cols[5]
                h24 = cols[6]
                d7 = cols[7]
                market_cap = cols[10]

                print(f"{rank} | {name} | {price} | {h1} | {h24} | {d7} | {market_cap}")

                # Append each row to data list
                all_data.append({
                    "Rank": rank,
                    "Name": name,
                    "Price": price,
                    "1h": h1,
                    "24h": h24,
                    "7d": d7,
                    "Market Cap": market_cap,
                    "Updated Time": time.strftime("%Y-%m-%d %H:%M:%S")
                })

            # Save data to CSV every loop (auto-creates file)
            df = pd.DataFrame(all_data)
            df.to_csv(filename, index=False)

            print(f"\nData saved to {filename}")

            # Instead of refresh (to prevent timeout), re-load safely
            driver.get(website)

        except Exception as e:
            print("Error while fetching data:", e)

        time.sleep(30)  # wait before next update

except KeyboardInterrupt:
    print("\nStopping live tracker...")
    driver.quit()
