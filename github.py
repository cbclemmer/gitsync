import os
import json
import requests
from git import Repo, exc

class Config:
    def __init__(self):
        CONFIG_FILE = "config.json"

        if not os.path.exists(CONFIG_FILE):
            raise Exception("Could not find config.json")

        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except:
            raise Exception("Could not read config.json")

        keys = [
            'github_api_key'
        ]

        for key in keys:
            if not key in config:
                raise Exception(f'Could not find key {key} in config')
        self.github_api_key = config['github_api_key']

def get_username(token):
    """ Fetches the GitHub username of the authenticated user """
    url = "https://api.github.com/user"
    headers = {'Authorization': f'token {token}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raises an error on a bad status
    return response.json()['login']

def get_repos_users(username, token):
    """ Fetches a list of repositories for a given user with all pages """
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/users/{username}/repos?page={page}&per_page=100&type=all"
        headers = {'Authorization': f'token {token}'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an error on a bad status
        page_data = response.json()
        if not page_data:
            break
        for repo in page_data:
            print(repo['name'])
            if not repo['fork']:
                repos.append(repo)
        page += 1
    return repos

def get_repos(username, token):
    """ Fetches a list of repositories using the search/repositories endpoint """
    repos = []
    page = 1
    query = f"user:{username} fork:true"  # Includes forks for completeness, adjust as needed
    while True:
        url = f"https://api.github.com/search/repositories?q={query}&page={page}&per_page=100"
        headers = {'Authorization': f'token {token}'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an error on a bad status
        page_data = response.json()['items']
        if not page_data:
            break
        for repo in page_data:
            if not repo['fork']:
                repos.append(repo)
        page += 1
    return repos

def clone_or_update_repo(repo, path):
    """ Clones or updates the repository based on its presence in the given path """
    repo_path = os.path.join(path, repo['name'])
    git_url = repo['clone_url']
    
    if os.path.exists(repo_path):
        try:
            print(f'Updating {repo_path}')
            local_repo = Repo(repo_path)
            current_commit = local_repo.head.commit.hexsha
            remote_commit = local_repo.remote().fetch()[0].commit.hexsha
            
            if current_commit != remote_commit:
                print(f"Updating {repo['name']}...")
                local_repo.remote().pull()
            else:
                print(f"{repo['name']} is up to date.")
        except exc.InvalidGitRepositoryError:
            print(f"Error: {repo_path} is not a git repository. Removing and cloning again...")
            os.system(f"rm -rf {repo_path}")
            Repo.clone_from(git_url, repo_path)
    else:
        print(f"Cloning {repo['name']}...")
        try:
            Repo.clone_from(git_url, repo_path)
        except Exception as e:
            print(e)

def main(token, path):
    """ Main function to fetch and update repositories """
    username = get_username(token)
    if not os.path.exists(path):
        os.makedirs(path)
    
    repos = get_repos(username, token)
    for repo in repos:
        clone_or_update_repo(repo, path)

if __name__ == "__main__":
    config = Config()
    main(config.github_api_key, 'github')
