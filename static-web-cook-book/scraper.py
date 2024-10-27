import time

import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

options = uc.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")


driver = uc.Chrome(options=options)


def get_page_content(page_key: str) -> str:
    from main import config

    root_url = config.pages.root
    page_path = getattr(config.pages, page_key, "/")
    full_url = str(root_url) + page_path
    driver.get(full_url)
    return driver.page_source


def scrape_page(page_key: str):
    property_links = []
    driver.get("https://uae.dubizzle.com/")

    try:
        wait = WebDriverWait(driver, 40)

        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        print("Page body loaded, now scrolling...")

        scroll_pause_time = 2
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            time.sleep(scroll_pause_time)

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print("Reached bottom of page.")
                break
            last_height = new_height

        categories = ["Property for Rent", "Property for Sale"]

        for category in categories:
            try:
                category_div = wait.until(EC.presence_of_element_located((By.XPATH, f"//div[h2[text()='{category}']]")))
                print(f"Found the category div for: {category}")

                category_div_html = category_div.get_attribute("outerHTML")
                print("category_div HTML:", category_div_html)

                view_all_link = driver.find_element(
                    By.XPATH,
                    f"//a[contains(text(), 'All in') and contains(@href, '{category.lower().replace(' ', '-')}')]",
                )
                href = view_all_link.get_attribute("href")

                full_url = "https://uae.dubizzle.com" + href if href.startswith("/") else href
                property_links.append(full_url)
                print(f"Added link for {category}: {full_url}")

            except NoSuchElementException as e:
                print(f"Could not find elements for category '{category}': {str(e)}")

        print(f"Collected links: {property_links}")

        for link in property_links:
            driver.get(link)
            print(f"Navigated to: {link}")

            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            # TODO: Add scraping logic here

            driver.back()

    except TimeoutException as e:
        print(f"TimeoutException: Could not find elements. {str(e)}")

    finally:
        driver.quit()


if __name__ == "__main__":
    driver.quit()
