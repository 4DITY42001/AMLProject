import pymongo
import numpy
from pymongo import MongoClient
import pandas as pd
import json


def send():
    
    client = pymongo.MongoClient(
        "mongodb+srv://user:hello123@project.kswnu.mongodb.net/project?retryWrites=true&w=majority:27017/")

    # Database Name
    db = client["project"]

    # Collection Name
    collection = db["Recognition"]
    path='/AEP_hourly.csv'
    df = pd.read_csv(path)
    data = df.to_dict('records')

    collection.insert_many(data, ordered=False)
    print("All the Data has been Exported to Mongo DB Server .... ")


send()

