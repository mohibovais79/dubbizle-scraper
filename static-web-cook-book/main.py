import json

from custom_types import ScrapingConfig  # Import the Pydantic models
from pydantic import ValidationError
from scraper import scrape_page

# Load the JSON data
with open("selectors.json", "r", encoding="utf-8") as file:
    data = json.load(file)

try:
    config = ScrapingConfig(**data)
except ValidationError as e:
    print("Configuration Error:", e.json())
    exit(1)

if __name__ == "__main__":
    scrape_page("home")  # Example: scrape the login page
