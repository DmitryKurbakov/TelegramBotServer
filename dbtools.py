from mongoengine import *
from pymongo import MongoClient
import re


def find_hackathons_by_title(text):
    client = MongoClient()

    db = client.HackathonAggregator
    sources = db.source

    match = re.compile(text)

    res = []

    cursor = sources.find({})
    for doc in cursor:
        temp = doc.get("title")
        if match.match(temp, re.IGNORECASE):
            res.append(doc)

    return res