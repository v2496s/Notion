import collections

import notion.block
import requests
import json


"""
зовніщня частина сторінки
потрібен юрл сторінки і токен
url = "https://api.notion.com/v1/pages/14217e1dfbc7478fb5cc5e5580d0a952"

headers = {
        "Authorization": "Bearer " + "secret_jlfaf0TOQsF1aOSLK4EpctPLLDNMAyVxQOAlf9JnSLB" ,
        "Content-Type": "application/json",
        "Notion-Version": "2021-05-13",
        "Accept": "application/json",
    }


#response = requests.get(url, headers=headers)


"""

"""
внутрішня части сторінки
потрібен юрл сторінки і токен
url = "https://api.notion.com/v1/blocks/14217e1dfbc7478fb5cc5e5580d0a952/children?page_size=100"

headers = {
        "Authorization": "Bearer " + "secret_jlfaf0TOQsF1aOSLK4EpctPLLDNMAyVxQOAlf9JnSLB" ,
        "Content-Type": "application/json",
        "Notion-Version": "2021-05-13",
        "Accept": "application/json",
    }


response = requests.get(url, headers=headers)

print(json.dumps(response.json(),indent=4))
"""
"""
token = "secret_4MGq67uxdnrouZgOVfKXAtvBu3WMhTT20eeVquuGAyq"
database_id = "8ebce70ab01d4b36a26b0b83d07a4cdd"
headers1 = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
        "Notion-Version": "2021-05-13",
        "Accept": "application/json",
    }

def get_list_of_pages(token):
    try:
        playload = {"page_size": 100}
        response = requests.post(
            f"https://api.notion.com/v1/databases/8ebce70ab01d4b36a26b0b83d07a4cdd/query",
            json=playload,
            headers=headers1,
        )

        return json.dumps(response.json(),indent=4)
    except:
        print("Error while fetching a user...")


print(get_list_of_pages(token))

"""


"""
import requests



def print_c(id):
    url = f"https://api.notion.com/v1/blocks/{id}"

    headers = {
        "Authorization": "Bearer " + "secret_jlfaf0TOQsF1aOSLK4EpctPLLDNMAyVxQOAlf9JnSLB",
        "Content-Type": "application/json",
        "Notion-Version": "2021-05-13",
        "Accept": "application/json",
    }
    response = requests.request("GET", url, headers=headers)

    print(json.dumps(response.json(), indent=4))


url = "https://api.notion.com/v1/blocks/dfbe5343-42a0-4eb5-960e-6db1cf2d36a5/children?page_size=100"

headers = {
        "Authorization": "Bearer " + "secret_jlfaf0TOQsF1aOSLK4EpctPLLDNMAyVxQOAlf9JnSLB",
        "Content-Type": "application/json",
        "Notion-Version": "2021-05-13",
        "Accept": "application/json",
    }

response = requests.get(url, headers=headers)

print(json.dumps(response.json(), indent=4))
for i in response.json()["results"]:
    print_c(i["id"])

"""


from notion.client import NotionClient
client = NotionClient(token_v2="e0a7c3d88dbc546477e14a9cbc9cf82df9f7cd41bc373d6fb0d4597d5ff67b8e15bee162a876a5117db338a8ceae29917ef887a52d65bd8acc93620f19b17d270776419890ddf3477e8bf7b755ea")
page = client.get_block("https://www.notion.so/Rozklad-14217e1dfbc7478fb5cc5e5580d0a952")

array_of_results = []
def rec2(arr):
    global array_of_results
    if arr.children:
        array_of_results.append({client.get_block(arr.id).type:client.get_block(arr.id)})
        for k in arr.children:
            rec2(k)
    else:
        array_of_results.append({client.get_block(arr.id).type: client.get_block(arr.id)})


for child in page.children:
    #print(child,child.id,child.type)
    rec2(child)
    pass





for i in array_of_results:
    print(i)



