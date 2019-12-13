import haversine
from haversine import haversine, Unit

from ..models import Address, Coordinates

# HOW MUCH NEAREST LOCATIONS TO SHOW CLIENT
NEAREST_LOCATION = 3

def parse_location(Location):
    coordinates_list_km = []
    location = [Location['lat'], Location['lng']]
    coordinates_list = Coordinates.objects.values_list('adress_id_id', 'lat', 'lng')
    
    for item in coordinates_list:
        if item[1] is not None and item[2] is not None:
            item_data = [item[1], item[2]]
            distances = haversine(tuple(location), tuple(item_data))
            tuple_data = [item[0], distances]
            coordinates_list_km.append(tuple(tuple_data))
    
    bubbleSort(coordinates_list_km)
    nearest_coordinates = coordinates_list_km[:NEAREST_LOCATION]
    return nearest_coordinates

def bubbleSort(arr):
    for i in range(len(arr)-1, 0, -1):
        for j in range(i):
            if arr[j][1] > arr[j+1][1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]

# address_id need for client (show in search list)
# address_id as link for shop_id (for parse request (search query client))