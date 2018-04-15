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
        str += '{}\n{}{}\n{}\n{}\n\n'.format(r['title'], p, re.sub(r'\s+', ' ', r['location']), r['time'], r['ref'])
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
