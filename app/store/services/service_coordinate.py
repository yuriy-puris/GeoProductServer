import requests
# from geopy.geocoders import Nominatim
from ..models import Address, Coordinates

# geolocator = Nominatim()
from pygeocoder import Geocoder

import urllib
import simplejson

def parse_coordinates():
    googleGeocodeUrl = 'https://maps.googleapis.com/maps/api/geocode/json?'
    list_address = Address.objects.values_list('address', 'id')
    for address in list_address:
        query = address[0].encode('utf-8')
        params = { 
            'address' : query, 
            'sensor' : 'false', 
        } 
        url = googleGeocodeUrl + urllib.parse.urlencode(params) + '&key=AIzaSyDybVMhuvhySYB54emzIuWjt1S44P-Z_hg'
        json_response  = urllib.request.urlopen(url) 
        response = simplejson.loads(json_response.read())
        if response['results']:
            model_coord = Coordinates(
                adress_id_id = address[1],
                lat = response['results'][0]['geometry']['location']['lat'],
                lng = response['results'][0]['geometry']['location']['lng']
            )
            model_coord.save()
        else:
            model_coord = Coordinates(
                adress_id_id = address[1],
                lat = None,
                lng = None
            )
            model_coord.save()
