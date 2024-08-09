### This code requires an ".ini" file, that reads the critical information in order to not have that as part of code. ####
### Este código requer um arquivo ".ini", que lê as informações críticas para não tê-las como parte do código. ####


import requests
import pandas as pd
import base64
import configparser

# configuration imported by the ".ini" file
# configuração importada pelo arquivo ".ini"

config = configparser.ConfigParser()
config.read('Access.ini')
token = config['credenciais']['token']
api_base_url = config['credenciais']['api_base_url']
owner = config['credenciais']['owner']
user = config['credenciais']['user']
repo = config['credenciais']['repo']
path = config['credenciais']['path']

url = f'{api_base_url}/users/{owner}/repos'
url2 = f'{api_base_url}/user/repos'
url3 = f'{api_base_url}/repos/{user}/{repo}/contents/{path}'
url4 = f'{api_base_url}/{user}/{repo}'

headers = {'Authorization':'Bearer ' + token ,
           'X-GitHub-Api_version': '2022-11-28'}

repos_list = []
for page_num in range(1, 6):
    try:
        url_page = f'{url}?page={page_num}'
        response = requests.get(url_page, headers=headers)
        repos_list.append(response.json())
    except:
        repos_list.append(None)

repos_name=[]
for page in repos_list:
    for repo in page:
        repos_name.append(repo['name'])

repos_language=[]
for page in repos_list:
    for repo in page:
        repos_language.append(repo['language'])

dados_amz = pd.DataFrame()
dados_amz['repository_name'] = repos_name
dados_amz['language'] = repos_language

dados_amz.to_csv('amazon.csv')

data = {
    'name': 'linguagens-utilizadas',
    'description': 'Repositorio com as linguagens de prog da Amazon',
    'private': False
}

response = requests.post(url2, json=data, headers=headers)
response.status_code

with open ('amazon.csv', 'rb') as file:
    file_content = file.read()
    encoded_content = base64.b64encode(file_content)


data = {
    'message': 'Adicionando um novo arquivo',
    'content': encoded_content.decode('utf-8')
}

response = requests.put(url3, json=data, headers=headers)
response.status_code