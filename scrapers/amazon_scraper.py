import requests
from typing import List
import sys
import os

# Ensure parent directory is in sys.path to import scraper_base
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scraper_base import BaseScraper, JobListing

class AmazonScraper(BaseScraper):
    def __init__(self):
        # Searching interns/students in Tel Aviv & Haifa as specified in the user's link
        self.api_url = "https://www.amazon.jobs/en/search.json?city=Tel+Aviv-Yafo&city=Haifa&employment_type=Interns"
        self.base_url = "https://www.amazon.jobs"
        
    def fetch_jobs(self) -> List[JobListing]:
        jobs = []
        try:
            # Pagination
            offset = 0
            limit = 100
            
            while True:
                url = f"{self.api_url}&offset={offset}&result_limit={limit}"
                response = requests.get(url, timeout=15)
                response.raise_for_status()
                data = response.json()
                
                job_list = data.get("jobs", [])
                if not job_list:
                    break
                    
                for job in job_list:
                    title = job.get("title", "")
                    job_id = str(job.get("id_icims", "") or job.get("id", ""))
                    job_path = job.get("job_path", "")
                    
                    desc = job.get("description", "")
                    basic_qual = job.get("basic_qualifications", "")
                    pref_qual = job.get("preferred_qualifications", "")
                    
                    full_desc = f"{desc}\n{basic_qual}\n{pref_qual}"
                    
                    # Already pre-filtered by 'Interns' employment_type via API,
                    # but doing a secondary check to be safe and save Gemini tokens.
                    search_text = (title + " " + full_desc).lower()
                    if "student" not in search_text and "intern" not in search_text and "סטודנט" not in search_text:
                        continue
                        
                    jobs.append(JobListing(
                        id=job_id,
                        title=title,
                        url=self.base_url + job_path,
                        description=full_desc,
                        company="Amazon"
                    ))
                    
                if len(job_list) < limit:
                    break
                
                offset += limit
                
        except Exception as e:
            print(f"Error fetching jobs from AmazonScraper: {e}")
            
        return jobs
