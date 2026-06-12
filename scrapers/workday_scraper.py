import requests
from bs4 import BeautifulSoup
from typing import List
import sys
import os

# Ensure parent directory is in sys.path to import scraper_base
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scraper_base import BaseScraper, JobListing

class WorkdayScraper(BaseScraper):
    def __init__(self, tenant: str, site: str, company: str, location_facets: List[str] = None):
        self.tenant = tenant
        self.site = site
        self.company = company
        self.location_facets = location_facets or []
        
        self.list_url = f"https://{tenant}.wd1.myworkdayjobs.com/wday/cxs/{tenant}/{site}/jobs"
        self.base_url = f"https://{tenant}.wd1.myworkdayjobs.com/en-US/{site}"
        self.api_base_url = f"https://{tenant}.wd1.myworkdayjobs.com/wday/cxs/{tenant}/{site}"
        
        # Build payload using searchText "Student Israel" to catch relevant jobs
        # For Intel we used specific IDs, but for a generic Workday scraper, searchText is safer.
        self.payload = {
            "appliedFacets": {},
            "limit": 20,
            "offset": 0,
            "searchText": "Student Israel"
        }
        
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0"
        }

    def fetch_jobs(self) -> List[JobListing]:
        jobs = []
        try:
            response = requests.post(self.list_url, json=self.payload, headers=self.headers, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            job_postings = data.get("jobPostings", [])
            
            for posting in job_postings:
                title = posting.get("title", "")
                external_path = posting.get("externalPath", "")
                job_id = external_path
                job_url = self.base_url + external_path
                
                # Pre-filter before hitting detailed API to save network calls
                if "student" not in title.lower() and "intern" not in title.lower() and "סטודנט" not in title:
                    continue
                    
                # Fetch details
                details_url = self.api_base_url + external_path
                details_response = requests.get(details_url, headers=self.headers, timeout=10)
                details_response.raise_for_status()
                details_data = details_response.json()
                
                raw_html_desc = details_data.get("jobPostingInfo", {}).get("jobDescription", "")
                clean_desc = BeautifulSoup(raw_html_desc, "html.parser").get_text(separator="\n").strip()
                
                jobs.append(JobListing(
                    id=self.company + "_" + job_id,
                    title=title,
                    url=job_url,
                    description=clean_desc,
                    company=self.company
                ))
        except Exception as e:
            print(f"Error fetching jobs from WorkdayScraper ({self.company}): {e}")
            
        return jobs
