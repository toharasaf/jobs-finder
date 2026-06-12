import requests

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

urls = {
    "Xsight": "https://xsightlabs.com/careers",
    "Tomer": "https://www.tomer-rs.co.il/article3.asp?tag=%D7%94%D7%A0%D7%93%D7%A1%D7%94",
    "Amazon": "https://www.amazon.jobs/en/search.json?location%5B%5D=israel&employment_type%5B%5D=Interns",
    "LinkedIn": "https://il.linkedin.com/jobs/search?keywords=mprest&location=Israel"
}

for name, url in urls.items():
    try:
        r = requests.get(url, headers=headers, timeout=5)
        print(f"[{name}] Status: {r.status_code}")
        print(f"[{name}] Content (first 200 chars): {r.text[:200]}")
    except Exception as e:
        print(f"[{name}] Error: {e}")
