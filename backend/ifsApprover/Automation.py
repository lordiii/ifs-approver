from ifsApprover import config
import requests

def trigger_github_actions():
    headers = {
        "Authorization": "Bearer " + config["GH_TOKEN"],
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": config["GH_API_VERSION"],
    }

    endpoint = config["GH_ENDPOINT"]

    payload = {
        "ref": config["GH_REF_BRANCH"],
    }

    r = requests.post(endpoint, json=payload, headers=headers)