import requests
import json
import re

url = "https://careers.wix.com/positions?locations=tel-aviv%2Cbeer-sheva&type=student"
r = requests.get(url)
print("Status:", r.status_code)
# Search for JSON data injected in HTML
match = re.search(r'window\.__INITIAL_STATE__\s*=\s*({.*?});', r.text)
if match:
    print("Found INITIAL_STATE!")
    data = json.loads(match.group(1))
    print(list(data.keys()))
else:
    print("No INITIAL_STATE found.")
    print("Length of HTML:", len(r.text))
    # Check for jobs API
    print("Any API endpoint mentioned?", re.findall(r'/api/[^\"]+', r.text)[:5])
