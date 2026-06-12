import sys
import os
from typing import List

# Ensure parent directory is in sys.path to import scraper_base
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scraper_base import BaseScraper, JobListing

class ElbitScraper(BaseScraper):
    def fetch_jobs(self) -> List[JobListing]:
        # Elbit blocks external API access returning 404 for Niloosoft requests
        print("ElbitScraper: API blocked. Requires Playwright/Selenium. Skipping for now.")
        return []
