import requests
from bs4 import BeautifulSoup
from typing import List
import sys
import os

# Ensure parent directory is in sys.path to import scraper_base
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scraper_base import BaseScraper, JobListing

class OracleScraper(BaseScraper):
    def __init__(self, api_url, job_url_base, company):
        # API URL for Oracle HCM Careers
        self.api_url = api_url
        self.job_url_base = job_url_base
        self.company = company
        
    def fetch_jobs(self) -> List[JobListing]:
        jobs = []
        try:
            offset = 0
            limit = 200
            
            while True:
                # Add offset and limit for pagination
                url = f"{self.api_url}&offset={offset}&limit={limit}"
                response = requests.get(url, timeout=15)
                response.raise_for_status()
                data = response.json()
                
                items = data.get("items", [])
                if not items:
                    break
                    
                requisition_list = items[0].get("requisitionList", [])
                if not requisition_list:
                    break
                    
                for req in requisition_list:
                    title = req.get("Title", "")
                    job_id = str(req.get("Id", ""))
                    location = req.get("PrimaryLocation", "")
                    
                    # The user specifically filtered by Location=Israel
                    if "Israel" not in location:
                        continue
                        
                    short_desc = req.get("ShortDescriptionStr", "") or ""
                    req_resp = req.get("ExternalResponsibilitiesStr", "") or ""
                    req_qual = req.get("ExternalQualificationsStr", "") or ""
                    
                    desc = f"{short_desc}\n{req_resp}\n{req_qual}"
                    
                    # Clean HTML from desc if any
                    desc = BeautifulSoup(desc, "html.parser").get_text(separator="\n").strip()
                    
                    # Pre-filter for student/intern to save Gemini API calls
                    search_text = (title + " " + desc).lower()
                    if "student" not in search_text and "intern" not in search_text and "סטודנט" not in search_text:
                        continue
                        
                    jobs.append(JobListing(
                        id=job_id,
                        title=title,
                        url=self.job_url_base + job_id,
                        description=desc,
                        company=self.company
                    ))
                    
                # If we received less than the limit, it means we reached the end
                if len(requisition_list) < limit:
                    break
                    
                offset += limit
                
        except Exception as e:
            print(f"Error fetching jobs from OracleScraper: {e}")
            
        return jobs
