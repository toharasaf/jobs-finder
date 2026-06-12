import sys
sys.stdout.reconfigure(encoding='utf-8')
import requests
from bs4 import BeautifulSoup
import urllib.parse
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

print("=== XSIGHT ===")
r_xsight = requests.get("https://xsightlabs.com/careers", headers=headers)
soup_x = BeautifulSoup(r_xsight.text, 'html.parser')
jobs = soup_x.find_all(lambda tag: tag.name == "div" and "job" in tag.get('class', [''])[0].lower())
print("Found job divs?", len(jobs))
# Print any URLs
urls = re.findall(r'https?://[^\s\"\']+', r_xsight.text)
api_urls = [u for u in urls if 'api' in u or '.json' in u]
print("API URLs:", api_urls[:5])

print("\n=== MPREST ===")
r_mprest = requests.get("https://www.mprest.com/careers/", headers=headers)
soup_m = BeautifulSoup(r_mprest.text, 'html.parser')
print("Found a tags:", len(soup_m.find_all('a')))
for a in soup_m.find_all('a', href=True):
    if 'job' in a['href'] or 'career' in a['href']:
        print(a['href'])

print("\n=== TOMER ===")
r_tomer = requests.get("https://www.tomer-rs.co.il/article3.asp?tag=" + urllib.parse.quote("הנדסה"), headers=headers)
soup_t = BeautifulSoup(r_tomer.text, 'html.parser')
print("Tomer title:", soup_t.title.string if soup_t.title else "No title")
for a in soup_t.find_all('a', href=True):
    if 'article' in a['href']:
        print(a['href'], a.text.strip())
