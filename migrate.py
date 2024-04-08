# Python Script to migrate the Repos

import requests
import subprocess

# Function to get repository details
def get_repo_details(owner, repo, token):
    headers = {
        'Authorization': f'token {token}'
    }
    url = f'https://api.github.com/repos/{owner}/{repo}'
    response = requests.get(url, headers=headers)
    return response.json()

# Function to create a new repository
def create_repo(name, description, token):
    headers = {
        'Authorization': f'token {token}'
    }
    payload = {
        'name': name,
        'description': description
    }
    url = 'https://api.github.com/user/repos'
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

# Function to clone repository
def clone_repo(repo_url):
    subprocess.run(['git', 'clone', repo_url])

# Function to push local repository to new repository
def push_to_new_repo(new_repo_url):
    subprocess.run(['git', 'remote', 'set-url', 'origin', new_repo_url])
    subprocess.run(['git', 'push', 'origin', '--all'])

# Main function
def main():
    # Source repository details
    source_owner = 'source_username'
    source_repo = 'repo_name'
    source_token = 'source_token'

    # Destination repository details
    dest_owner = 'destination_username'
    dest_repo = 'repo_name'
    dest_token = 'destination_token'

    # Get source repository details
    source_repo_details = get_repo_details(source_owner, source_repo, source_token)

    # Create a new repository under destination account
    new_repo = create_repo(dest_owner, dest_repo, dest_token)

    # Clone source repository locally
    clone_repo(source_repo_details['clone_url'])

    # Push local repository to new repository
    push_to_new_repo(source_repo_details['clone_url'], new_repo['clone_url'])

if __name__ == "__main__":
    main()
