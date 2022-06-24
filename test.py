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
import re


url = "https://www.notion.so/Compendium-1a30571cac244510b0013c0ef7543a25"


z1 = 'https://s3.us-west-2.amazonaws.com'

print(z1[0:18])
#https://s3.us-west
