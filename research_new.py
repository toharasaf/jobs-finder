import requests
import json

headers = {'User-Agent': 'Mozilla/5.0'}

urls = {
    "Monday (Greenhouse)": "https://boards-api.greenhouse.io/v1/boards/mondaycom/jobs",
    "Wix (Greenhouse)": "https://boards-api.greenhouse.io/v1/boards/wix/jobs",
    "CheckPoint (Comeet)": "https://www.comeet.co/careers-api/2.0/company/59.006/jobs", # Comeet usually needs the company UID
    "Microsoft": "https://gcsservices.careers.microsoft.com/search/api/v1/search"
}

for name, url in urls.items():
    try:
        r = requests.get(url, headers=headers, timeout=5)
        print(f"[{name}] Status: {r.status_code}")
        if r.status_code == 200:
            print(f"  Snippet: {r.text[:100]}")
    except Exception as e:
        print(f"[{name}] Error: {e}")
