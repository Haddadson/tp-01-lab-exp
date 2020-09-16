import sys
import requests
from json import dump
from json import loads
import datetime
import time
from dateutil import relativedelta

def run_query(json, headers):  
    print("Executando query...")
    request = requests.post('https://api.github.com/graphql', json=json, headers=headers)
    
    while (request.status_code != 200):
      print("Erro ao chamar API, tentando novamente...")
      print("Query failed to run by returning code of {}. {}. {}".format(request.status_code, json['query'],json['variables']))
      time.sleep(2)
      request = requests.post('https://api.github.com/graphql', json=json, headers=headers)
    
    return request.json()

query = """
query laboratorio {
 search (query:"stars:>1000", type:REPOSITORY, first:5{AFTER}) {
    pageInfo{
        hasNextPage
        endCursor
    }
    nodes {
      ... on Repository {
        nameWithOwner
        createdAt
        stargazers{
          totalCount
        }
        pullRequests(states: MERGED){
          totalCount
        }
        releases{
          totalCount
        }
        updatedAt
        primaryLanguage{
          name
        }
        closedIssues : issues(states: CLOSED){
          totalCount
        }
        totalIssues: issues{
          totalCount
        }
      }
    }
  }
}
"""

finalQuery = query.replace("{AFTER}", "")

json = {
    "query":finalQuery, "variables":{}
}

#chave de autenticação do GitHub
headers = {"Authorization": "Bearer  >>INSERIR CHAVE DO GITHUB AQUI<<"} 

total_pages = 1

print("Pagina -> 1")
result = run_query(json, headers)

nodes = result['data']['search']['nodes']
next_page  = result["data"]["search"]["pageInfo"]["hasNextPage"]

#paginação
while (next_page and total_pages < 200):
    total_pages += 1
    print("Pagina -> ", total_pages)
    cursor = result["data"]["search"]["pageInfo"]["endCursor"]
    next_query = query.replace("{AFTER}", ", after: \"%s\"" % cursor)
    json["query"] = next_query
    result = run_query(json, headers)
    nodes += result['data']['search']['nodes']
    next_page  = result["data"]["search"]["pageInfo"]["hasNextPage"]

#inserindo cabeçalho de identificação de dados ao csv
print("Gravando cabeçalho CSV...")
with open(sys.path[0] + "\\ResultadoSprint2.csv", 'a+') as the_file:
        the_file.write("nameWithOwner" + ";" + "stargazers/totalCount" + ";" 
        + "createdAt" + ";" + "repositoryAge" + ";" + "pullRequests/totalCount" + ";" 
        + "releases/totalCount" + ";" + "updatedAt" + ";" + "primaryLanguage/name" + ";" 
        + "closedIssues/totalCount" + ";" + "totalIssues/totalCount" + ";" 
        + "closedIssues/totalIssues (%)\n")

#salvando os dados em ResultadoSprint2.csv
print("Gravando linhas CSV...")
for node in nodes:
    if node['primaryLanguage'] is None:
        primary_language = "None"
    else:
        primary_language = str(node['primaryLanguage']['name'])

    datetime_now = datetime.datetime.now()
    datetime_created_at = datetime.datetime.strptime(node['createdAt'], '%Y-%m-%dT%H:%M:%SZ')
    repository_age = relativedelta.relativedelta(datetime_now, datetime_created_at).years
    closed_issues = node['closedIssues']['totalCount']
    total_issues = node['totalIssues']['totalCount']

    if total_issues == 0:
      closed_issues_ratio = "-"
    else:
      closed_issues_ratio = str("{0:.2f}".format(closed_issues / total_issues * 100))

    with open(sys.path[0] + "\\ResultadoSprint2.csv", 'a+') as the_file:
        the_file.write(node['nameWithOwner'] + ";" + str(node['stargazers']['totalCount']) + ";" 
        + datetime_created_at.strftime('%d/%m/%y %H:%M:%S') + ";" + str(repository_age) + ";" 
        + str(node['pullRequests']['totalCount']) + ";"
        + str(node['releases']['totalCount']) + ";" 
        + datetime.datetime.strptime(node['updatedAt'], '%Y-%m-%dT%H:%M:%SZ').strftime('%d/%m/%y %H:%M:%S') + ";" 
        + primary_language + ";" 
        + str(closed_issues) + ";" 
        + str(total_issues) + ";"
        + str(closed_issues_ratio) + "\n")

print("Finalizando...")