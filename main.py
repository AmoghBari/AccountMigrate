import requests
import json

def migrate_repository(source_owner, source_repo, destination_owner, destination_repo, source_token, destination_token):
    # Get the contents of the repository
    headers = {"Authorization": f"token {source_token}"}
    response = requests.get(f"https://api.github.com/repos/{source_owner}/{source_repo}/contents", headers=headers)
    if response.status_code != 200:
        print(f"Failed to get repository contents from {source_owner}/{source_repo}")
        return

    contents = response.json()

    # Create the destination repository
    headers = {
        "Authorization": f"token {destination_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {
        "name": destination_repo,
        "private": True  # You can set this to False if you want the repository to be public
    }
    response = requests.post(f"https://api.github.com/user/repos", headers=headers, json=payload)
    if response.status_code != 201:
        print(f"Failed to create repository {destination_repo} in {destination_owner}'s account")
        return

    print(f"Repository {destination_repo} created successfully in {destination_owner}'s account")

    # Clone each file and directory from the source repository to the destination repository
    for item in contents:
        if item["type"] == "file":
            # Get the contents of the file
            response = requests.get(item["download_url"], headers=headers)
            if response.status_code == 200:
                # Create the file in the destination repository
                payload = {
                    "message": f"Migration: Copy {item['name']} from {source_owner}/{source_repo}",
                    "content": response.content.decode("utf-8")
                }
                response = requests.put(f"https://api.github.com/repos/{destination_owner}/{destination_repo}/contents/{item['name']}", headers=headers, json=payload)
                if response.status_code != 201:
                    print(f"Failed to create file {item['name']} in {destination_owner}/{destination_repo}")
                else:
                    print(f"File {item['name']} created successfully in {destination_owner}/{destination_repo}")
            else:
                print(f"Failed to get contents of file {item['name']} from {source_owner}/{source_repo}")
        elif item["type"] == "dir":
            # Create an empty directory in the destination repository
            payload = {
                "message": f"Migration: Create directory {item['name']} from {source_owner}/{source_repo}",
                "content": ""
            }
            response = requests.put(f"https://api.github.com/repos/{destination_owner}/{destination_repo}/contents/{item['name']}", headers=headers, json=payload)
            if response.status_code != 201:
                print(f"Failed to create directory {item['name']} in {destination_owner}/{destination_repo}")
            else:
                print(f"Directory {item['name']} created successfully in {destination_owner}/{destination_repo}")

# Example usage
source_owner = "source_username"
source_repo = "source_repository_name"
destination_owner = "destination_username"
destination_repo = "destination_repository_name"
source_token = "source_account_token"
destination_token = "destination_account_token"

migrate_repository(source_owner, source_repo, destination_owner, destination_repo, source_token, destination_token)
