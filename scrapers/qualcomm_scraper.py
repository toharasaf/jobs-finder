import sys
import os
from typing import List

# Ensure parent directory is in sys.path to import scraper_base
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scraper_base import BaseScraper, JobListing

class QualcommScraper(BaseScraper):
    def fetch_jobs(self) -> List[JobListing]:
        # Qualcomm uses Eightfold AI API which blocks basic requests (returns 403)
        print("QualcommScraper: API blocked (403). Requires Playwright/Selenium. Skipping for now.")
        return []
