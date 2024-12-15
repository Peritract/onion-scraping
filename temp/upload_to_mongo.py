import json

from pymongo.mongo_client import MongoClient

if __name__ == "__main__":

    uri = f"mongodb+srv://admin:ElusiveWelshGoblin@satire-cluster.ydiot.mongodb.net/?retryWrites=true&w=majority&appName=satire-cluster"

    with open("all_articles.json", "r") as f:
        data = json.load(f)

    client = MongoClient(uri)

    db = client.satire

    collection = db.satire

    res = collection.insert_many(data)

    print(res)
    print(res.inserted_ids)