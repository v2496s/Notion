import requests, json
from pymongo import MongoClient
from notion.client import NotionClient

cluster = MongoClient(
    "mongodb://notionAPI:pass@cluster0-shard-00-00.phkvz.mongodb.net:27017,cluster0-shard-00-01.phkvz.mongodb.net:27017,cluster0-shard-00-02.phkvz.mongodb.net:27017/?ssl=true&replicaSet=atlas-rkmjvp-shard-0&authSource=admin&retryWrites=true&w=majority"
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
        url+= "blocks/"
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

        return json.dumps(response.json(), indent=4)
    except:
        print("Error while fetching a user...")

# readDB(database_id,token)


def get_children_of_page(tokenv2,url):
    arr = []
    client = NotionClient(token_v2=tokenv2)
    page = client.get_block(url)
    for child in page.children:
        print(child)
        arr.append(child.id)
    return arr


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

def get_page_by_id(id,token):
    #try:



        res = ""
        url = create_url("bl")


        url += id + "/children?page_size=100"
        response = requests.get(url, headers=create_headers(token))
        #insert_to_mongo(response.json())
        res = json.dumps(response.json(),indent=4)


        return res
    #except:
    #    print("Error while fetching a page...")


# get_page_by_id("secret_jlfaf0TOQsF1aOSLK4EpctPLLDNMAyVxQOAlf9JnSLB", "14217e1dfbc7478fb5cc5e5580d0a952")


def get_list_of_pages(token):
    try:
        response = requests.post(
            create_url("li"),
            headers=create_headers(token),
        )
        #insert_to_mongo(response.json())
        return json.dumps(response.json(),indent=4)
    except:
        print("Error while fetching a user...")


# get_list_of_pages(headers)


from flask import Flask, render_template, url_for, request


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

            print(result)
        print(token,database_id)
        return render_template("show.html",result=result)

    return render_template("retrieve_a_block.html")


@app.route("/retrieve_a_page", methods=["POST", "GET"])
def retrieve_page():
    result = "there should be json"
    if request.method == ("POST"):
        token = request.form.get("integration")
        page = request.form.get("page")
        if token and page :
            result = get_page_by_id(page, token)
            print(result)
        return render_template("show.html", result=result)

    return render_template("retrieve_a_page.html")


@app.route("/retrieve_a_list", methods=["POST", "GET"])
def retrieve_list():
    result = "тут мав бути джейсон"
    if request.method == ("POST"):
        token = request.form.get("integration")
        if len(token) > 0:
            result = get_list_of_pages(token)
            #print(result)
        return render_template("show.html", result=result)

    return render_template("retrieve_a_list.html")


@app.route("/show")
def show():
    return render_template("show.html")


if __name__ == "__main__":
    app.run(debug=True)


