from flask import Flask, render_template, url_for, request
import requests, json
from pymongo import MongoClient
from notion.client import NotionClient
array_of_results = []
first_time=True


cluster = MongoClient(
    "mongodb://notionAPI:Zxcvbnm1238!@cluster0-shard-00-00.phkvz.mongodb.net:27017,cluster0-shard-00-01.phkvz.mongodb.net:27017,cluster0-shard-00-02.phkvz.mongodb.net:27017/?ssl=true&replicaSet=atlas-rkmjvp-shard-0&authSource=admin&retryWrites=true&w=majority"
     )
db = cluster["ForApi"]
col = db["Block"]

token = "token"  #secret_jlfaf0TOQsF1aOSLK4EpctPLLDNMAyVxQOAlf9JnSLB
database_id = "database_id"  #8ebce70ab01d4b36a26b0b83d07a4cdd



def create_headers(token):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
        "Notion-Version": "2021-05-13",
        "Accept": "application/json",
    }
    return headers

def create_url(type):
    url = "https://api.notion.com/v1/"
    if type == "db":
        url += "search/"
    elif type == "pg":
        url += "pages/"
    elif type == "li":
        url += "search/"
    elif type == "bl":
        url += "blocks/"
    return url


def insert_to_mongo(data):
    #col.insert_one({"json": data})
    pass


def readDB(database_id, token):
    try:
        playload = {"page_size": 100}
        response = requests.post(
            f"https://api.notion.com/v1/databases/{database_id}/query",
            json=playload,
            headers=create_headers(token),
        )
        print(json.dumps(response.json(),indent=4))
        return response.json()
    except:
        print("Error while fetching a user...")

# readDB(database_id,token)



def get_block_by_id(block_id,token):
    url = f"https://api.notion.com/v1/blocks/{block_id}"

    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
        "Notion-Version": "2021-05-13",
        "Accept": "application/json",
    }
    response = requests.request("GET", url, headers=headers)
    #print(json.dumps(response.json(), indent=4))
    return json.dumps(response.json(), indent=4)



def get_page_blocks(arr,token):
    arr2 = []
    for i in arr:
        arr2.append(get_block_by_id(i, token))
        json_o = json.loads(get_block_by_id(i, token))
        obj = json_o.items()
        for k, v in obj:
            if k == "type":
                if v == "column_list":
                    arr2.append(column_list(i))
    return arr2



def column_list(block_id):


    url = f"https://api.notion.com/v1/blocks/{block_id}/children?page_size=100"

    headers = {
        "Authorization": "Bearer " + "secret_jlfaf0TOQsF1aOSLK4EpctPLLDNMAyVxQOAlf9JnSLB",
        "Content-Type": "application/json",
        "Notion-Version": "2021-05-13",
        "Accept": "application/json",
    }

    response = requests.request("GET", url, headers=headers)

    #print(json.dumps(response.json(), indent=4))
    return json.dumps(response.json())

def get_page_by_id(v2,url):
    global array_of_results
    array_of_results = []
    client = NotionClient(
        token_v2=v2)
    page = client.get_block(url)


    def rec2(arr):
        global array_of_results
        if arr.children:
            array_of_results.append({client.get_block(arr.id).type: client.get_block(arr.id)})
            for k in arr.children:
                rec2(k)
        else:
            array_of_results.append({client.get_block(arr.id).type: client.get_block(arr.id)})

    for child in page.children:
        rec2(child)


    return array_of_results


def get_list_of_pages(token):
    try:
        response = requests.post(
            create_url("li"),
            headers=create_headers(token),
        )
        return response.json()
    except:
        print("Error while fetching a user...")


# get_list_of_pages(headers)



def get_content_from_db(json_str):
    arr_rows = []
    index = 0
    for i in json_str["results"]:
        index += 1
        arr_rows.append(f" --------------- {index} row ---------------")
        for key , value in i["properties"].items():
            for k,v in value.items():
                if k == "rich_text" or k == "title":
                    arr_rows.append(v)
    return arr_rows


def get_urls(json_str):

    arr = []
    for j in json_str["results"]:
            arr.append(j["url"])
    print(arr)
    return arr



app = Flask(__name__)



@app.route("/")
def home():
    return render_template("main.html")


@app.route("/retrieve_a_block", methods=["POST", "GET"])
def retrieve_block():
    result = "there should be json"
    if request.method == ("POST"):
        token = request.form.get("integration")
        database_id = request.form.get("database")
        if token and database_id:
            result = readDB(database_id,token)
            array_of_results = get_content_from_db(result)
        return render_template("show.html",result=array_of_results)

    return render_template("retrieve_a_block.html")


@app.route("/retrieve_a_page", methods=["POST", "GET"])
def retrieve_page():
    global array_of_results
    if request.method == ("POST"):
        v2 = request.form.get("v2")
        url = request.form.get("url")
        if v2 and url:
            not_ready_results = get_page_by_id(v2, url)
            result = not_ready_results.copy()
        array_of_results = []
        return render_template("show.html", result=result)

    return render_template("retrieve_a_page.html")


@app.route("/retrieve_a_list", methods=["POST", "GET"])
def retrieve_list():
    array_of_results2 = []
    array_of_results = []
    num_of_page = 0



    if request.method == ("POST"):
        token = request.form.get("integration")
        v2 = request.form.get("v2")
        if token and v2:
            not_ready_urls = get_list_of_pages(token)


            arr_of_pages = get_urls(not_ready_urls)

            for i in arr_of_pages:
                num_of_page+=1
                array_of_results2.append(f"{num_of_page} Page {i}")
                array_of_results2.append(get_page_by_id(v2,i))
            result = array_of_results2.copy()
            array_of_results = []
            for page in result:
                print(page)
        return render_template("show.html", result=result)

    return render_template("retrieve_a_list.html")


@app.route("/show")
def show():
    return render_template("show.html")


if __name__ == "__main__":
    app.run(debug=True)
    print("start")

