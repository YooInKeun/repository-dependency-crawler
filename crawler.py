from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import base64
import json

API_TOKEN = ''
GITHUB_BASE_URL = "https://github.com"
GITHUB_API_BASE_URL = 'https://api.github.com'
USER_NAME = 'YooInKeun'

def get_api():
    repo_request_url = f'{GITHUB_API_BASE_URL}/users/{USER_NAME}/repos?page=1&per_page=100' # 페이지당 최대 100개 가능
    headers = {'Authorization': f'token {API_TOKEN}'}
    repos = requests.get(repo_request_url, headers = headers).json()

    for repo in repos:
        repo_url = repo['html_url']
        repo_path = repo_url.replace(GITHUB_BASE_URL, '')

        master_request_url = f'{GITHUB_API_BASE_URL}/repos{repo_path}/branches/master' # master -> main일 수도 
        master_data = requests.get(master_request_url, headers = headers).json()

        tree_sha = master_data['commit']['commit']['tree']['sha']
        file_path_request_url = f'{GITHUB_BASE_URL}{repo_path}/tree-list/{tree_sha}'
    
        headers['accept'] = 'application/json'
        file_paths = requests.get(file_path_request_url, headers = headers).json()
        dependency_file_paths = []

        # 테스트용으로 package.json 만 우선 진행
        for file_path in file_paths['paths']:
            if 'package.json' in file_path:
                    dependency_file_paths.append(file_path)
        
        if len(dependency_file_paths) < 1:
            continue

        for dependency_file in dependency_file_paths:
            file_content_request_url = f'{GITHUB_API_BASE_URL}/repos{repo_path}/contents/{dependency_file}'
            file_raw_content = requests.get(file_content_request_url, headers = headers).json()['content']
            
            try:
                file_content = json.loads(base64.b64decode(file_raw_content))
                for key in file_content['dependencies']:
                    print(key)
            except:
                print('#####json load 실패#####')

if __name__ == "__main__":
    get_api()
