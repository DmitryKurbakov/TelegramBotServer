import re
from haversine import haversine
import api
import googlemaps


def form_message(res):
    p = ""
    str = ""
    for r in res:

        if r['preview'] != "":
            p = r['preview'] + '\n'
        #str += '{}\n{}{}\n{}\n{}\n\n'.format(r['title'], p, re.sub(r'\s+', ' ', r['location']), r['time'], r['ref'])
        str += '{}\n{}{}\n{}\n\n'.format(r['title'], p, re.sub(r'\s+', ' ', r['location']), r['ref'])
    return str


def is_point_near(user_lyon, data_lyon):
    if haversine(user_lyon, data_lyon) < 200:
        return True
    else:
        return False


def get_geocode(text):
    gmaps = googlemaps.Client(key=api.gkey)
    geo = gmaps.geocode(re.sub(r'\s+', ' ', text))

    return (geo[0]['geometry']['location']['lat'], geo[0]['geometry']['location']['lng'])


def find_hackathons_by_title(text, docs):
    match = re.compile(text)

    res = []

    for doc in docs:
        temp = doc.get("title")
        if temp.lower() == text.lower() or text.lower() in temp.lower():
            res.append(doc)

    return res


def find_hackathons_by_location(text, docs):
    res = []
    if len(docs) > 0:
        user_geocode = get_geocode(text)

        for doc in docs:
            try:
                temp = doc.get("geocode")
                data_point = (temp[0]['geometry']['location']['lat'], temp[0]['geometry']['location']['lng'])
                if (temp != "" and temp != 1.0) and data_point == user_geocode:
                    res.append(doc)
            except:
                continue

    return res


def find_hackathons_by_country(text, docs):
    res = []
    if len(docs) > 0:
        user_geocode = get_geocode(text)

        for doc in docs:
            try:
                temp = doc.get("country_geocode")
                data_point = (temp[0]['geometry']['location']['lat'], temp[0]['geometry']['location']['lng'])
                if (temp != "" and temp != 1.0) and is_point_near(user_geocode, data_point):
                    res.append(doc)
            except:
                continue

    return res


def find_hackathons_by_type(text, docs):
    res = []
    for doc in docs:
        temp_list = doc.get('area')
        for temp in temp_list:
            if text == temp or (text == 'economy' and temp == 'economy'):
                res.append(doc)
    return res
