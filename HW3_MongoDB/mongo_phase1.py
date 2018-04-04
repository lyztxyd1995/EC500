import json, pymongo
from pymongo import MongoClient
file = open("/Users/yizeliu/Downloads/airports.json", 'r')
data = json.loads(file.read())
connection = MongoClient(port=27017)
database = connection.airports
posts = database.posts.insert_many(data)
print("finished")