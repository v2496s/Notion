import requests, json
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