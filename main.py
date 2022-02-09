


#офіційне джерело для бази даних/будь-якого блоку

import requests, json
token = "secret_jlfaf0TOQsF1aOSLK4EpctPLLDNMAyVxQOAlf9JnSLB"
database_id = "ccbdaa1d1711437eabb4878ff518786e"

headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2021-05-13"
}


def readDB(database_id,headers):
    readUrl = f"https://api.notion.com/v1/databases/{database_id}/query"
    res = requests.request("POST", readUrl, headers=headers)

    data = res.json()
    #print(res.status_code)
    #print(res.text)

    with open('./db.json', 'w', encoding='utf8') as f:
        json.dump(data, f,indent=4, ensure_ascii=False)

readDB(database_id,headers)
"""

#неофіційне джерело
from notion.client import NotionClient

client = NotionClient(token_v2="d0afc93e6c403df8d1da462215d6b3639f11491188212242a61ae86998bc7f8cbb9fd02e83eb77bc999ab8e3ecd63a73f528e6e85870a0fcd96c173dd42587c82794e54d60924a95f5bbdd636dcd")

page = client.get_block("https://www.notion.so/asd-1a30571cac244510b0013c0ef7543a25")

page.title = "Я пургаміст"
for child in page.children:
    print(child)

"""