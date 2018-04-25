from mongoengine import *
from pymongo import MongoClient
import re
import api
import googlemaps
import helpers

def find_hackathons_by_title(text):
    client = MongoClient()

    db = client.HackathonAggregator
    sources = db.source

    match = re.compile(text)

    res = []

    cursor = sources.find({})
    for doc in cursor:
        temp = doc.get("title")
        if temp.lower() == text.lower():
            res.append(doc)

    return res


def find_hackathon_by_location(text):
    client = MongoClient()

    db = client.HackathonAggregator
    sources = db.source

    res = []
    user_geocode = helpers.get_geocode(text)
    cursor = sources.find({})
    for doc in cursor:

        try:
            temp = doc.get("geocode")
            data_point = (temp[0]['geometry']['location']['lat'], temp[0]['geometry']['location']['lng'])
            if (temp != "" and temp != 1.0) and helpers.is_point_near(user_geocode, data_point):
                res.append(doc)
        except:
            continue

    return res