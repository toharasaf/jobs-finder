import requests
from bs4 import BeautifulSoup
import re

url = "https://careers.wix.com/positions?locations=tel-aviv%2Cbeer-sheva&type=student"
r = requests.get(url)

soup = BeautifulSoup(r.text, 'html.parser')
jobs = soup.find_all(lambda tag: tag.name == "a" and "position" in tag.get("href", ""))
print(f"Found {len(jobs)} position links.")
if jobs:
    print(jobs[0].get("href"))
    
# Let's search for "jobs" or "positions" in script tags
for script in soup.find_all('script'):
    if script.string and "Student" in script.string:
        print("Found Student in script!")
        print(script.string[:200])
