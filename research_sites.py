import requests
from bs4 import BeautifulSoup
import urllib.parse

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

urls = [
    ("mPrest", "https://www.mprest.com/careers/"),
    ("Xsight", "https://xsightlabs.com/careers"),
    ("Tomer", "https://www.tomer-rs.co.il/article3.asp?tag=" + urllib.parse.quote("הנדסה"))
]

for name, url in urls:
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Look for comeet or lever in iframe/script
        for tag in soup.find_all(['iframe', 'script']):
            src = tag.get('src', '')
            if 'comeet' in src or 'lever' in src or 'greenhouse' in src:
                print(f"[{name}] Found ATS: {src}")
        
        # Look for job links
        print(f"[{name}] Links with 'job' or 'career' or 'משרה':")
        for a in soup.find_all('a', href=True):
            if 'job' in a['href'].lower() or 'career' in a['href'].lower() or 'משר' in a.text or 'position' in a['href'].lower():
                print("  ", a['href'], "->", a.text.strip()[:30])
    except Exception as e:
        print(f"[{name}] Failed: {e}")
