import sys
import os
from typing import List

# Ensure parent directory is in sys.path to import scraper_base
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scraper_base import BaseScraper, JobListing

class WixScraper(BaseScraper):
    def fetch_jobs(self) -> List[JobListing]:
        # Wix is a dynamic SPA that requires Playwright
        print("WixScraper: Website requires dynamic rendering (Playwright/Selenium). Skipping for now.")
        return []
