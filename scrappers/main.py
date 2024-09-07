import json
from db_connection import conn
from utils.console import console

path_to_json = "/root/hackathon6/data/channels.json"

with open(path_to_json, "r") as json_file:
    data = json.load(json_file)

channels = data["result"]["channels"]

# print 10 most followed channels, sort by "followerCount" parameter

channels = sorted(channels, key=lambda x: x["createdAt"], reverse=False)

for channel in channels[:10]:
    console.print(channel)
