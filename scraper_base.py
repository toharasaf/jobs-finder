from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

@dataclass
class JobListing:
    id: str  # Unique identifier for the job (often URL or external ID)
    title: str
    url: str
    description: str
    company: str = "Unknown"

class BaseScraper(ABC):
    """
    Abstract base class for all job site scrapers.
    """
    @abstractmethod
    def fetch_jobs(self) -> List[JobListing]:
        """
        Fetches a list of new jobs from the specific site.
        Should return a list of JobListing objects.
        """
        pass
