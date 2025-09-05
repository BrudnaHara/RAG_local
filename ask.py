#!/usr/bin/env python3
import sys, json, requests
URL = "http://127.0.0.1:8000/ask"
q = " ".join(sys.argv[1:]).strip() or "Co to jest test penetracyjny?"
body = {"query": q, "k": 3, "max_ctx_chars": 1500}
r = requests.post(URL, headers={"Content-Type":"application/json"}, data=json.dumps(body), timeout=120)
print(r.text.strip())
