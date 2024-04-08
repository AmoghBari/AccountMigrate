import requests
import json
import os

# GitHub API access tokens for source and destination accounts
source_token = os.getenv('your_source_token')
destination_token = os.getenv('your_destination_token')

# Source and destination repository information
source_repo_name = 'repo_name'
destination_repo_name = 'repo-name'
source_username = 'username'
destination_username = 'username'

# Headers for GitHub API requests
source_headers = {
    'Authorization': f'token {source_token}',
    'Accept': 'application/vnd.github.v3+json'
}

destination_headers = {
    'Authorization': f'token {destination_token}',
    'Accept': 'application/vnd.github.v3+json'
}

# Get source repository information
source_repo_url = f'https://api.github.com/repos/{source_username}/{source_repo_name}'
response = requests.get(source_repo_url, headers=source_headers)
source_repo_data = response.json()

# Determine if source repository is private or public
source_repo_private = source_repo_data.get('private', False)

# Create destination repository
destination_repo_url = f'https://api.github.com/user/repos'
payload = {
    'name': destination_repo_name,
    'private': source_repo_private
}
response = requests.post(destination_repo_url, headers=destination_headers, data=json.dumps(payload))
destination_repo_data = response.json()

# Get source repository contents
source_repo_contents_url = f'https://api.github.com/repos/{source_username}/{source_repo_name}/contents'
response = requests.get(source_repo_contents_url, headers=source_headers)
source_contents = response.json()

# Clone repository contents
for content in source_contents:
    if isinstance(content, dict) and content.get('type') == 'file':
        file_url = content['url']
        file_response = requests.get(file_url, headers=source_headers)
        file_data = file_response.json()
        file_content = requests.get(file_data['download_url']).content

        destination_file_url = f'https://api.github.com/repos/{destination_username}/{destination_repo_name}/contents/{content["path"]}'
        destination_payload = {
            'message': 'Migration',
            'content': file_content.decode('utf-8'),
            'branch': 'main'
        }
        requests.put(destination_file_url, headers=destination_headers, data=json.dumps(destination_payload))

print("Repository migration completed successfully!")
