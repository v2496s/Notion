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

# Obtain the `token_v2` value by inspecting your browser cookies on a logged-in (non-guest) session on Notion.so
client = NotionClient(token_v2="<token_v2>")

# Replace this URL with the URL of the page you want to edit
page = client.get_block("https://www.notion.so/myorg/Test-c0d20a71c0944985ae96e661ccc99821")

print("The old title is:", page.title)

# Note: You can use Markdown! We convert on-the-fly to Notion's internal formatted text data structure.
page.title = "The title has now changed, and has *live-updated* in the browser!"
