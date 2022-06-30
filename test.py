"""import requests, json
from pymongo import MongoClient
from notion.client import NotionClient

cluster = MongoClient(
    "mongodb://notionAPI:Zxcvbnm1238!@cluster0-shard-00-00.phkvz.mongodb.net:27017,cluster0-shard-00-01.phkvz.mongodb.net:27017,cluster0-shard-00-02.phkvz.mongodb.net:27017/?ssl=true&replicaSet=atlas-rkmjvp-shard-0&authSource=admin&retryWrites=true&w=majority"
    #mongodb+srv://notionAPI:Zxcvbnm1238!@cluster0.phkvz.mongodb.net/?retryWrites=true&w=majority
    #mongodb+srv://notionAPI:Zxcvbnm1238!@cluster0.phkvz.mongodb.net/ForApi?retryWrites=true&w=majority
    #mongodb://notionAPI:Zxcvbnm1238!@cluster0-shard-00-00.phkvz.mongodb.net:27017,cluster0-shard-00-01.phkvz.mongodb.net:27017,cluster0-shard-00-02.phkvz.mongodb.net:27017/?ssl=true&replicaSet=atlas-rkmjvp-shard-0&authSource=admin&retryWrites=true&w=majority
 )
db = cluster["ForApi"]
col = db["Block"]

col.insert_one({"_id": 0})

"""

"""
import boto3
import os
import requests

client = boto3.client('s3')


bucket = ""

url2 = "https://www.youtube.com/watch?v=IMQEjZHhOEw&ab_channel=%F0%9D%96%8E%F0%9D%96%99%F0%9D%96%86%F0%9D%96%92%F0%9D%96%8E"

response = requests.get(url2)

open("v.mp4", "wb").write(response.content)



"""


"""
url = "https://www.notion.so/Compendium-1a30571cac244510b0013c0ef7543a25"


z1 = 'https://s3.us-west-2.amazonaws.com'

print(z1[0:18])

"""


import requests


def get_type(block):
    if block["type"]:
        return block["type"]
    else:
        return False

def get_content(block, type):
    if block[f"{type}"]:
        return {type: block[f"{type}"]}
    else:
        return False


def detect_children(block):
    if block["has_children"]:
        if block["has_children"] == True:
            return True
        else:
            return False
    else:
        return False


#https://api.notion.com/v1/blocks/block_id/children?page_size=100


url = "https://api.notion.com/v1/blocks/14217e1dfbc7478fb5cc5e5580d0a952/children?page_size=100"
headers = {
    "Authorization": "Bearer " + "secret_jlfaf0TOQsF1aOSLK4EpctPLLDNMAyVxQOAlf9JnSLB",
    "Content-Type": "application/json",
    "Notion-Version": "2021-05-13",
    "Accept": "application/json",
}


response = (requests.get(url, headers=headers).json()).copy()




array_of_results = []

def get_p(dump):
    global array_of_results

    def get_children(block_id):
        url = f"https://api.notion.com/v1/blocks/{block_id}/children?page_size=100"
        headers = {
            "Authorization": "Bearer " + "secret_jlfaf0TOQsF1aOSLK4EpctPLLDNMAyVxQOAlf9JnSLB",
            "Content-Type": "application/json",
            "Notion-Version": "2021-05-13",
            "Accept": "application/json",
        }
        for i in requests.get(url, headers=headers).json()["results"]:
            rec(i)

    def rec(block):
        array_of_results.append({ get_type(block) : get_content(block, get_type(block)) })

        if detect_children(block):
            get_children(block["id"])


    for i in dump["results"]:
        if detect_children(i):
            rec(i)
        else:
            array_of_results.append(get_content(i, get_type(i)))




    return array_of_results




for i in get_p(response):
    print(i)

