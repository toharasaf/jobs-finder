import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0'}
urls = {
    "Rafael": "https://career.rafael.co.il/search/f/T2LAdH6H9H1H5/1/",
    "Nova": "https://www.novami.com/results/?freetext=Student+&location=israel",
    "Qualcomm": "https://careers.qualcomm.com/careers?query=Student&start=0&location=Israel",
    "Elbit": "https://elbitsystemscareer.com/Recruitment-Page/#job-search",
    "Applied": "https://www.appliedmaterials.com/il/en/careers/students-early-career.html"
}

for name, url in urls.items():
    try:
        r = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(r.text, 'html.parser')
        print(f"[{name}] Title:", soup.title.string if soup.title else "No Title")
        # Check for comeet / greenhouse / lever / hunter
        for tag in soup.find_all(['script', 'iframe']):
            src = tag.get('src', '')
            if any(ats in src.lower() for ats in ['comeet', 'greenhouse', 'lever', 'niloosoft']):
                print(f"  ATS found: {src}")
    except Exception as e:
        print(f"[{name}] Error: {e}")
