import requests
from bs4 import BeautifulSoup
from typing import List
import sys
import os

# Ensure parent directory is in sys.path to import scraper_base
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scraper_base import BaseScraper, JobListing

class ExampleScraper(BaseScraper):
    """
    An example scraper. 
    You need to adapt this to a real website by updating the URL and CSS selectors.
    """
    def __init__(self):
        self.url = "https://example-jobs-site.com/jobs?category=student"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def fetch_jobs(self) -> List[JobListing]:
        jobs = []
        try:
            # Example parsing (uncomment and use when you have a real URL and structure):
            # response = requests.get(self.url, headers=self.headers, timeout=10)
            # response.raise_for_status()
            # soup = BeautifulSoup(response.text, 'html.parser')
            # 
            # for job_card in soup.select('.job-card'):
            #     title = job_card.select_one('.title').text.strip()
            #     link = job_card.select_one('a')['href']
            #     description = job_card.select_one('.description').text.strip()
            #     company = job_card.select_one('.company-name').text.strip()
            #     job_id = link # Often the URL itself is a good unique ID
            #     
            #     jobs.append(JobListing(id=job_id, title=title, url=link, description=description, company=company))
            
            # For demonstration, returning a dummy job
            print("Running ExampleScraper... (Please replace with real scraping logic)")
            jobs.append(JobListing(
                id="dummy-job-789",
                title="משרת סטודנט פיתוח פייתון",
                url="https://example.com/job/789",
                description="דרוש/ה סטודנט/ית למדעי המחשב לפיתוח אוטומציות ב-Python. ידע ב-Web Scraping ו-API - יתרון משמעותי.",
                company="Tech Co"
            ))
            
        except Exception as e:
            print(f"Error fetching jobs from ExampleScraper: {e}")
            
        return jobs
