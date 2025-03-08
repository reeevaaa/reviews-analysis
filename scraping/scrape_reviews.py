from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

# Setup ChromeDriver
service = Service("chromedriver.exe")  # Ensure correct path to chromedriver
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-gpu")

def scrape_reviews():
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 10)
    csv_filename = "raw_reviews.csv"

    try:
        # Navigate to the restaurant page
        driver.get("https://www.zomato.com/mumbai/ettarra-coffee-house-1-juhu/reviews")
        time.sleep(5)

        # Handle cookie consent popup
        try:
            cookie_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label*='accept']")))
            cookie_button.click()
        except:
            pass  # Ignore if cookie consent is not present

        with open(csv_filename, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Reviews Count", "Followers", "Rating", "Review Text"])
            print("✅ Created CSV file for reviews")
            page = 1
            next_button_xpath = "//*[@id='root']/div/main/div/section[4]/div/div/section/div[3]/div[2]/div/a[6]"
            
            while True:
                print(f"Scraping page {page}...")
                time.sleep(2)
                
                x = 1
                y = 1
                while y <= 5: 
                    try:
                        # Extract review details using dynamic XPaths
                        name_xpath = f"//*[@id='root']/div/main/div/section[4]/div/div/section/div[2]/section[{x}]/div/div/a/p"
                        reviews_count_xpath = f"//*[@id='root']/div/main/div/section[4]/div/div/section/div[2]/section[{x}]/div/div/section/span[1]"
                        followers_xpath = f"//*[@id='root']/div/main/div/section[4]/div/div/section/div[2]/section[{x}]/div/div/section/span[2]"
                        rating_xpath = f"//*[@id='root']/div/main/div/section[4]/div/div/section/div[2]/div[6]/div/div[1]/div/div/div[1]"
                        review_xpath = f"//*[@id='root']/div/main/div/section[4]/div/div/section/div[2]/p[{y}]"
                        
                        x = x + 3
                        y = y + 1

                        name = driver.find_element(By.XPATH, name_xpath).text.strip()
                        reviews_count = driver.find_element(By.XPATH, reviews_count_xpath).text.strip()
                        followers = driver.find_element(By.XPATH, followers_xpath).text.strip()
                        rating = driver.find_element(By.XPATH, rating_xpath).text.strip()
                        review = driver.find_element(By.XPATH, review_xpath).text.strip()
                        
                        writer.writerow([name, reviews_count, followers, rating, review])
                        print(f"Added review from {name}")

                    except Exception as e:
                        print(f"Error extracting review at section {x}: {e}")
                        continue

                print(f"✅ Page {page} scraped successfully")

                # Navigate to next page
                try:
                    next_button = driver.find_element(By.XPATH, next_button_xpath)
                    print(next_button)
                    if not next_button.is_displayed() or not next_button.is_enabled():
                        print("Reached last page")
                        break

                    driver.execute_script("arguments[0].scrollIntoView();", next_button)
                    time.sleep(1)
                    print('next!')
                    driver.execute_script("arguments[0].click();", next_button)
                    page += 1
                    time.sleep(2)

                    # Update the next button XPath after the first click
                    next_button_xpath = "//*[@id='root']/div/main/div/section[4]/div/div/section/div[3]/div[2]/div/a[7]"

                except Exception as e:
                    print(f"No more pages available: {e}")
                    break

    except Exception as e:
        print(f"❌ Critical error: {e}")
    finally:
        driver.quit()
        print(f"✅ Scraping complete. Reviews saved to {csv_filename}")

if __name__ == "__main__":
    scrape_reviews()
