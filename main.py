from flask import Flask, render_template, request
import requests, json, re
from pymongo import MongoClient
from notion.client import NotionClient
array_of_results = []
first_time=True

password = ""

#cluster = MongoClient(
#    f"mongodb://notionAPI:{password}@cluster0-shard-00-00.phkvz.mongodb.net:27017,cluster0-shard-00-01.phkvz.mongodb.net:27017,cluster0-shard-00-02.phkvz.mongodb.net:27017/?ssl=true&replicaSet=atlas-rkmjvp-shard-0&authSource=admin&retryWrites=true&w=majority"
#     )
#db = cluster["ForApi"]
#col = db["Block"]

token = "token"
database_id = "database_id"


def name_from_url(url):
    return url[22:len(url) - 33]

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
        url += "blocks/"
    elif type == "li":
        url += "search/"
    else:
        return
    return url


def insert_to_mongo(data):
    #col.insert_one({"json": data})
    pass


def get_database_by_id(database_id, token):
    try:
        playload = payload = {
        "page_size": 100
        }

        response = requests.post(
            f"https://api.notion.com/v1/databases/{database_id}/query",
            json=playload,
            headers=create_headers(token),
        )

        return response.json()
    except:
        print("Error: Can`t read a database")


def get_block_by_id(block_id,token):
    url = f"https://api.notion.com/v1/blocks/{block_id}"

    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
        "Notion-Version": "2021-05-13",
        "Accept": "application/json",
    }

    response = requests.request("GET", url, headers=headers)
    return json.dumps(response.json(), indent=4)


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


def get_content_from_db(json_str):
    try:
        arr_rows = []
        index = 0
        for i in json_str["results"]:
            index += 1
            arr_rows.append(f" --------------- {index} row ---------------")
            for key, value in reversed(i["properties"].items()):
                for k,v in value.items():
                    if k == "rich_text" or k == "title":
                        arr_rows.append(v)
        return arr_rows
    except:
        arr_rows= ["Error: Can't read Database"]
        return  arr_rows


def get_urls(json_str):
    arr = []
    for j in json_str["results"]:
            arr.append(j["url"])
    return arr


def image_download(block,name,index):
    for k,v in block.items():
        if v.source[0:18] == "https://s3.us-west":
            response = requests.get(v.source)
            name = name_from_url(name)
            open(f"{name}-image-{index}.png", "wb").write(response.content)
        return v.source


def video_download(block,name,index):
    for k,v in block.items():
        if v.source[0:18] == "https://s3.us-west":
            response = requests.get(v.source)
            name = name_from_url(name)
            open(f"{name}-video-{index}.mp4", "wb").write(response.content)
        return v.source


def block_sort(arr,name):
    index = 0
    for block in arr:
        for block_type in block:
            if block_type == "image":
                index+=1
                image_download(block,name,index)
            elif block_type == "video":
                index+=1
                video_download(block,name,index)


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("main.html")


@app.route("/retrieve_a_block", methods=["POST", "GET"])
def retrieve_block():
    if request.method == "POST":
        integration_token = request.form.get("integration")
        database_id = request.form.get("database")
        if token and database_id:
            result = get_database_by_id(database_id,integration_token)
            database_content = get_content_from_db(result)
            return render_template("show.html", result=database_content)
        else:
            err = "Error: Invalid input"
            return render_template("show.html", result=err)
    else:
        pass

    return render_template("retrieve_a_block.html")


@app.route("/retrieve_a_page", methods=["POST", "GET"])
def retrieve_page():

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




    if request.method == "POST":
        integration = request.form.get("integration")
        page_id = request.form.get("page_id")
        if integration and page_id:

            headers = create_headers(integration)
            url = create_url("pg")
            url += page_id
            url += "/children?page_size=100"
            page = (requests.get(url, headers=headers).json()).copy()
            global array_of_results

            for i in page["results"]:
                if detect_children(i):
                    rec(i)
                else:
                    array_of_results.append(get_content(i, get_type(i)))


            #block_sort(array_of_results,url)
            return render_template("show.html", result=array_of_results)
        else:
            return render_template("show.html", result=["Error: Invalid Input"])
    else:
        pass
    return render_template("retrieve_a_page.html")


@app.route("/retrieve_a_list", methods=["POST", "GET"])
def retrieve_list():
    array_of_results2 = []
    num_of_page = 0
    if request.method == "POST":
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

            for page in result:
                print(page)
        return render_template("show.html", result=result)
    return render_template("retrieve_a_list.html")


@app.route("/show")
def show():
    return render_template("show.html")


if __name__ == "__main__":
    app.run(debug=True,host ="0.0.0.0")

