
from notion.client import NotionClient
client = NotionClient(token_v2="d0afc93e6c403df8d1da462215d6b3639f11491188212242a61ae86998bc7f8cbb9fd02e83eb77bc999ab8e3ecd63a73f528e6e85870a0fcd96c173dd42587c82794e54d60924a95f5bbdd636dcd")

# Replace this URL with the URL of the page you want to edit
page = client.get_block("https://www.notion.so/Rozklad-14217e1dfbc7478fb5cc5e5580d0a952")

print("The old title is:", page.title)

# Note: You can use Markdown! We convert on-the-fly to Notion's internal formatted text data structure.

