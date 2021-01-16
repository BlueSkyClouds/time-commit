from pprint import pprint
import requests
import json
import os

# POST /repos/:GITHUB_USERNMAE/:GITHUB_REPO/dispatches
# Replace with your info...

GITHUB_USERNMAE = "BlueskyClouds"
GITHUB_REPO = "time-commit"

AUTH_TOKEN = os.environ["GITHUB_REPO_TOKEN"]
DATA = {}

url = "https://api.github.com/repos/"+GITHUB_USERNMAE+"/"+GITHUB_REPO+"/dispatches"
headers = {
    "Authorization": "token "+AUTH_TOKEN,
    "Accept": "application/vnd.github.everest-preview+json",
}
data = {"event_type": "start_action", "client_payload": DATA}

requests.post(url, headers=headers, data=json.dumps(data))
