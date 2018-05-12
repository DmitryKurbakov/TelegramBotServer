import pymongo
import re
import api
from sshtunnel import SSHTunnelForwarder
from datetime import datetime

server = SSHTunnelForwarder(
    api.MONGO_HOST,
    ssh_username=api.MONGO_USER,
    ssh_password=api.MONGO_PASS,
    remote_bind_address=('localhost', 27017)
)

server.start()


def get_hackathon_types():
    client = pymongo.MongoClient('localhost', server.local_bind_port)  # server.local_bind_port is assigned local port
    db = client[api.MONGO_DB]
    db_types = db.types

    types = []

    doc = db_types.find({})

    for it in doc:
        #print("Types from database: " + str(it.keys()))
        types = list(it.keys())
        types.remove('_id')

    return types


def get_hackathons_by_relevance(relevance):
    client = pymongo.MongoClient('localhost', server.local_bind_port)  # server.local_bind_port is assigned local port
    db = client[api.MONGO_DB]
    sources = db.source

    res = []

    cursor = sources.find({})

    for doc in cursor:
        if relevance == 2:
            res.append(doc)
        else:
            temp_str = doc.get('time').split('-')
            if len(temp_str) < 3:
                continue
            start_date_str = '{} {} {}'.format(temp_str[0], temp_str[1], temp_str[2])
            start_date = datetime.strptime(start_date_str, '%Y %m %d')
            today_date = datetime.now()
            if relevance == 0:
                if start_date > today_date:
                    res.append(doc)
                    continue
            elif relevance == 1:
                if start_date <= today_date:
                    res.append(doc)
    return res


def get_hackathons_in_two_days():
    client = pymongo.MongoClient('localhost', server.local_bind_port)  # server.local_bind_port is assigned local port
    db = client[api.MONGO_DB]
    sources = db.source

    res = []

    cursor = sources.find({})

    for doc in cursor:
        temp_str = doc.get('time').split('-')
        if len(temp_str) < 3:
            continue
        start_date_str = '{} {} {}'.format(temp_str[0], temp_str[1], temp_str[2])
        start_date = datetime.strptime(start_date_str, '%Y %m %d')
        today_date = datetime.now()

        if start_date.day - 2 == today_date.day\
                and start_date.month == today_date.month\
                and start_date.year == today_date.year:
            res.append(doc)
    return res
