import urllib.request
import json

url = "http://localhost:8000/api/users/register/"
data = {
    "email": "testpy2@example.com",
    "username": "testpy2",
    "password": "password123",
    "user_type": "CONSUMER",
    "store_name": ""
}
req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
try:
    with urllib.request.urlopen(req) as f:
        print(f.read().decode())
except urllib.error.HTTPError as e:
    print("ERROR:", e.read().decode())
