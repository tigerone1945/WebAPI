import json
import requests
import msal
import traceback
import pandas as pd
from pandas import json_normalize

#Graph API configuration
graph_url = 'https://graph.microsoft.com'
tenant_id = "43733a2a-598f-444e-9463-5867551baef8"
client_id = "5b835048-c033-4c01-9d97-523717f030f7"
client_secret = "4E38Q~BbBV1p-3e0AjL4djzwd4GG1EmRnGNhma0F"

def msgraph_auth():
    authority = 'https://login.microsoftonline.com/' + tenant_id
    scope = ['https://graph.microsoft.com/.default']

    try:
        app = msal.ConfidentialClientApplication(client_id, authority = authority, client_credential = client_secret)
        access_token = app.acquire_token_for_client(scopes = scope)
        if access_token['access_token']:
#            print('New access token retrieved....')
#             access_token['access_token'] = "eyJ0eXAiOiJKV1QiLCJub25jZSI6IllMdmFNZTkydnBGc0g1RVcyUm44VUJTUW9YaU5rSWdkZUtjZWlyZjBXRlUiLCJhbGciOiJSUzI1NiIsIng1dCI6Ii1LSTNROW5OUjdiUm9meG1lWm9YcWJIWkdldyIsImtpZCI6Ii1LSTNROW5OUjdiUm9meG1lWm9YcWJIWkdldyJ9.eyJhdWQiOiIwMDAwMDAwMy0wMDAwLTAwMDAtYzAwMC0wMDAwMDAwMDAwMDAiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC81NWYwYTEzYi0xZjBmLTRkNWUtYjU5MC05MWRjOWYwN2U2OTIvIiwiaWF0IjoxNjgzNzczNDY0LCJuYmYiOjE2ODM3NzM0NjQsImV4cCI6MTY4Mzg2MDE2NCwiYWNjdCI6MCwiYWNyIjoiMSIsImFpbyI6IkFWUUFxLzhUQUFBQTA3ckVueXhDQmRqb0xpTFlaZVQ4ZW85NDhNaDVZTzhuNnU2QlpIK0xVSE5WR2RhK25MdHkxVE9NK29HWDJ0clE2WkhMdXVnODB1eWFlbTMvdlI1eDdORmYrZkdZbU5YcGNrbnNBTnBLbjc0PSIsImFtciI6WyJwd2QiLCJtZmEiXSwiYXBwX2Rpc3BsYXluYW1lIjoiR3JhcGggRXhwbG9yZXIiLCJhcHBpZCI6ImRlOGJjOGI1LWQ5ZjktNDhiMS1hOGFkLWI3NDhkYTcyNTA2NCIsImFwcGlkYWNyIjoiMCIsImZhbWlseV9uYW1lIjoiTWFlZGEiLCJnaXZlbl9uYW1lIjoiWW96byIsImlkdHlwIjoidXNlciIsImlwYWRkciI6IjI3LjEzNi4xNDkuMTk1IiwibmFtZSI6Illvem8gTWFlZGEiLCJvaWQiOiJlYjM5Zjk2ZS1hNjRhLTRiOTktYjBmNS1kZTA4NTEzNGZmYmMiLCJvbnByZW1fc2lkIjoiUy0xLTUtMjEtNDI1ODQ1NDExNi0zMTQyODQxNzAtMTg2MzA1NDgxNS02NjkxIiwicGxhdGYiOiI1IiwicHVpZCI6IjEwMDMwMDAwODM1NUQwNUYiLCJyaCI6IjAuQVNzQU82SHdWUThmWGsyMWtKSGNud2Zta2dNQUFBQUFBQUFBd0FBQUFBQUFBQUFyQU9jLiIsInNjcCI6Im9wZW5pZCBwcm9maWxlIFVzZXIuUmVhZCBlbWFpbCIsInNpZ25pbl9zdGF0ZSI6WyJrbXNpIl0sInN1YiI6ImJIczQ4cFN0d1hlYVhXd093S1JSU2U1Z01RS2ljUW9OeUtVVDBVY2tzb3MiLCJ0ZW5hbnRfcmVnaW9uX3Njb3BlIjoiQVMiLCJ0aWQiOiI1NWYwYTEzYi0xZjBmLTRkNWUtYjU5MC05MWRjOWYwN2U2OTIiLCJ1bmlxdWVfbmFtZSI6InltYWVkYUB0b3lvLWVuZy5jb20iLCJ1cG4iOiJ5bWFlZGFAdG95by1lbmcuY29tIiwidXRpIjoicW82VEZ6YVc1VUdrX1lObHdZQmJBQSIsInZlciI6IjEuMCIsIndpZHMiOlsiYjc5ZmJmNGQtM2VmOS00Njg5LTgxNDMtNzZiMTk0ZTg1NTA5Il0sInhtc19jYyI6WyJDUDEiXSwieG1zX3NzbSI6IjEiLCJ4bXNfc3QiOnsic3ViIjoidUlia3k3SDhjYmlRTjhsX0VXQ2k4NDRQYlVqaGhiSDlyMzhvbDV4LXpPRSJ9LCJ4bXNfdGNkdCI6MTM1MTgzOTM5M30.kQ7SoklalE2huiWz8ZhqQLuwCmo7YVOKCiMgCe-1I9t31XhP58vkh8GbiYu0SMjsWf5A8rMmxdAMw3moZmAJxpX7ONu5XQowkAl8iW7ayXPEOrElD-yIrkKr_b9_lrHn7sxxP7v2Gi9MbyRmQOMQbbNO65VHj_IclDq18ifFFp9AtLVFbnPbii9_xe0AO10MQcoAOZ3nzpfYDELuh9QBjZE7ePmTvw-Qhzteuu8fCZYiQK2pdaOW5T1y4JQqO6Q9fqh4miaepUjWrBDQHwRCdGsyVhcU0NlI5lYwY1l9K19Qbk0PeWk5hu_JX8J1HxnBgEUkZIFypdw-gAEPIdWMKA"
            request_headers = {'Authorization': 'Bearer ' + access_token['access_token']}
#             print(access_token['access_token'])
            return request_headers
        else:
            print('ERROR: No "access_token" in the result.')
    except:
        print('ERROR: Could not acquired authorization token. Check your tenant_id, client_id and client_secret.')
        traceback.print_exc()
        exit(1)

def msgraph_request(resource,request_headers):
    results = requests.get(resource, headers = request_headers)
    return results

def show_users():

    # ユーザー一覧を取得するエンドポイントのパス
    q = "users"

    # Graphへのクエリ実行
    request_headers = msgraph_auth()
    results = msgraph_request(graph_url + '/v1.0/' + q, request_headers)
    return results

def get_ad_all_groups():

    q = "groups"

    request_headers = msgraph_auth()
    results = msgraph_request(graph_url + '/v1.0/' + q, request_headers)
    return results

def get_ad_group_menbers(id):

#    group_id = "00068c6f-3ce3-48de-a47c-5b7217de4e08"
#    param1 = "members/microsoft.graph.user?$count=true&$orderby=displayName&$search="
#    param2 = "displayName:Pr"
#    param3 = "&$select=displayName,idConsistencyLevel: eventual"
    group_id = id
    param = "/members"

    q = "groups/" + group_id + param
#    q = "groups/" + group_id  + param1 + '"' + param2 + '"' + param3
#    print(q)

    request_headers = msgraph_auth()
    results = msgraph_request(graph_url + '/v1.0/' + q, request_headers)
    return results

