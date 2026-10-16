import urllib.request
import json
import sys

RENDER_API_KEY = "rnd_YaTq9nAEAF5MYozvkCbJXKAZ0Nzn"
OWNER_ID = "tea-db7fceqvcj2c73derfa0"
REPO_URL = "https://github.com/molytrolai/Moly-The-Gioi-Chuot-Chui"
NEON_DATABASE_URL = "postgresql://neondb_owner:npg_QUak1c0dzVqy@ep-autumn-bar-a1n8y84y.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"

def create_service():
    url = "https://api.render.com/v1/services"
    headers = {
        "Authorization": f"Bearer {RENDER_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = {
        "type": "web_service",
        "name": "molyvn",
        "ownerId": OWNER_ID,
        "repo": REPO_URL,
        "branch": "main",
        "autoDeploy": "yes",
        "serviceDetails": {
            "env": "docker",
            "region": "singapore",
            "plan": "free",
            "envVars": [
                {
                    "key": "DATABASE_URL",
                    "value": NEON_DATABASE_URL
                },
                {
                    "key": "PORT",
                    "value": "8080"
                },
                {
                    "key": "PYTHONUNBUFFERED",
                    "value": "1"
                }
            ]
        }
    }

    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            print("Successfully created Render Service!")
            print(json.dumps(data, indent=2))
            return data
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}:")
        err_body = e.read().decode("utf-8")
        print(err_body)
        return None

if __name__ == "__main__":
    create_service()
