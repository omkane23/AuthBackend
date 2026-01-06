from pymongo import MongoClient

client = MongoClient("mongodb+srv://omkane:<omkane123>@cluster0.t66872i.mongodb.net/?appName=Cluster0")
db = client["test_db"]

print("MongoDB Connected Successfully")
