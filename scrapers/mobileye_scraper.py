import requests
from typing import List
import sys
import os

# Ensure parent directory is in sys.path to import scraper_base
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scraper_base import BaseScraper, JobListing

class MobileyeScraper(BaseScraper):
    def __init__(self):
        # Lever API for Mobileye
        self.api_url = "https://api.eu.lever.co/v0/postings/mobileye?mode=json"
        
    def fetch_jobs(self) -> List[JobListing]:
        jobs = []
        try:
            response = requests.get(self.api_url, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            for posting in data:
                title = posting.get("text", "")
                desc = posting.get("descriptionPlain", "")
                
                # Pre-filter: We only want student/intern roles to save AI API calls
                # since Mobileye returns ALL jobs via this API endpoint.
                search_text = (title + " " + desc).lower()
                if "student" not in search_text and "intern" not in search_text and "סטודנט" not in search_text:
                    continue
                    
                jobs.append(JobListing(
                    id=posting.get("id", ""),
                    title=title,
                    url=posting.get("hostedUrl", ""),
                    description=desc,
                    company="Mobileye"
                ))
                
        except Exception as e:
            print(f"Error fetching jobs from MobileyeScraper: {e}")
            
        return jobs
