import requests, json

from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://notionAPI:pro100pro1238@cluster0.phkvz.mongodb.net/ForApi?retryWrites=true&w=majority")
db = cluster["ForApi"]
col = db["Block"]



token = "your token"
database_id = "your db id"
headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2021-05-13"
}

def readDB(database_id,headers):

        Url = f"https://api.notion.com/v1/databases/{database_id}"
        response = requests.request("GET", Url, headers=headers)
        col.insert_one({"json": response.json()})
        #print(response.json())
        with open('./db.json', 'w', encoding='utf8') as f:
            json.dump(response.json(), f, ensure_ascii=False)
        return response.json()

readDB(database_id,headers)

def get_page_by_id(token, id, ):
    try:
        Url = "https://api.notion.com/v1/pages/" + id
        response = requests.request("GET", Url, headers=headers)
        col.insert_one({"json": response.json()})
        #print(response.json())
        with open('./db.json', 'w', encoding='utf8') as f:
            json.dump(response.json(), f, indent=4, ensure_ascii=False)
        return response.json()
    except:
        print("Error while fetching a page...")

#get_page_by_id("secret_jlfaf0TOQsF1aOSLK4EpctPLLDNMAyVxQOAlf9JnSLB", "14217e1dfbc7478fb5cc5e5580d0a952")

def get_list_of_pages(headers):
    try:
        response = requests.post('https://api.notion.com/v1/search',headers=headers,)
        col.insert_one({"json": response.json()})
        #print(response.json())
        with open('./db.json', 'w', encoding='utf8') as f:
            json.dump(response.json(), f, indent=4, ensure_ascii=False)
        return response.json()
    except:
        print("Error while fetching a user...")

#get_list_of_pages(headers)



#window for user

"""
from tkinter import *


import tkinter as tk
from tkinter import ttk

window = tk.Tk()

window.title("Notion Authorization")
window.minsize(300, 400)


def clickMe():
    #label.configure(text='Hello ' + name.get())
    pass


label = ttk.Label(window, text="Authorize to your account in Notion")
label.grid(column=1, row=0, sticky=W,padx=200)

login = tk.StringVar()
passw = tk.StringVar()

nameEntered = ttk.Entry(window, width=50, textvariable=login)
nameEntered1 = ttk.Entry(window, width=50, textvariable=passw)
nameEntered.grid(column=1, row=1)

nameEntered1.grid(column=1, row=2)
label2 = ttk.Label(window, text="")
label2.grid(column=1, row=3)
button = ttk.Button(window, text="Sign in", command=clickMe)
button.grid(column=1, row=4)
window.mainloop()


"""
import unittest

class TestStringMethods(unittest.TestCase):
    def test_correct_db(self):
        expected ={'object': 'database', 'id': '8ebce70a-b01d-4b36-a26b-0b83d07a4cdd', 'cover': None, 'icon': None, 'created_time': '2022-02-12T17:45:00.000Z', 'last_edited_time': '2022-02-12T17:46:00.000Z', 'title': [], 'properties': {'Tags': {'id': 'Yq><', 'name': 'Tags', 'type': 'multi_select', 'multi_select': {'options': []}}, 'qw': {'id': 'title', 'name': 'qw', 'type': 'title', 'title': {}}}, 'parent': {'type': 'page_id', 'page_id': '1a30571c-ac24-4510-b001-3c0ef7543a25'}, 'url': 'https://www.notion.so/8ebce70ab01d4b36a26b0b83d07a4cdd'}
        actual = readDB(database_id,headers)
        self.assertEqual(actual, expected)

    def test_invalid_id_db(self):
        actual = readDB("invalid_id", headers)
        expected = {'object': 'error', 'status': 400, 'code': 'validation_error', 'message': 'path failed validation: path.database_id should be a valid uuid, instead was `"invalid_id"`.'}
        self.assertEqual(actual, expected)

    def test_invalid_headers_db(self):
        actual = readDB(database_id, "invalid_headers")
        expected = "Error while fetching a block..."
        print(expected)
        self.assertEqual(actual, expected)


