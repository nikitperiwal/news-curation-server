from pymongo import MongoClient
from secret_keys import mongo_username, mongo_password

mongo_url = f"mongodb+srv://{mongo_username}:{mongo_password}@shortly.autde.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(mongo_url)


def persist_to_mongo(items: list, collection_name: str, db_name: str = "news_db"):
    """
    Stores the curated news articles into the MongoDB.

    Parameters
    ----------
    items           -> The list of news articles to be stored.
    db_name         -> Name of the MongoDB database to store the articles in.
    collection_name -> Name of the collection to store the articles in.
    """
    global client

    db = client[db_name]
    collection = db[collection_name]
    collection.insert_many(items)


def read_from_mongo(collection_name: str, db_name: str = "news_db"):
    """
    Retrieves the stored news articles into the MongoDB.

    Parameters
    ----------
    db_name         -> Name of the MongoDB database to read the articles from.
    collection_name -> Name of the collection to read the articles from.

    Returns
    -------
    cursor -> the cursor to the selected collection.
    """
    global client

    db = client[db_name]
    cursor = db[collection_name].find()
    return cursor


def drop_from_mongo(collection_name: str, db_name: str = "news_db"):
    """
    Drops collection from database in MongoDB.

    Parameters
    ----------
    db_name         -> Name of the MongoDB database to read the articles from.
    collection_name -> Name of the collection to read the articles from.

    Returns
    -------
    items -> The list of news articles stored in db.
    """
    global client

    db = client[db_name]
    db[collection_name].drop()
