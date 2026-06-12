import sys
import os
from typing import List

# Ensure parent directory is in sys.path to import scraper_base
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scraper_base import BaseScraper, JobListing

class TomerScraper(BaseScraper):
    def fetch_jobs(self) -> List[JobListing]:
        # Tomer requires handling Hebrew encoding perfectly and might block basic requests
        print("TomerScraper: The website requires dynamic rendering (Playwright/Selenium). Skipping for now.")
        return []
