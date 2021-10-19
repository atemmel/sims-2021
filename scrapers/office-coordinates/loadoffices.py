import json
from geopy.geocoders import Nominatim


cities = []
data = {}

with open('../../datasets/offices.json', 'r',encoding="UTF-8") as file:
    data = json.loads(file.read())

    for i in data:
        c = i["visit-adress"]["city"]
        if not c in cities:
            cities.append(c)
            
with open("../../datasets/officeCoordinates.json", "w", encoding="UTF-8",newline='\n' ) as file:
    office_coords = []
    for ptr in range (len(cities)):
        address=cities[ptr]
        geolocator = Nominatim(user_agent="Your_Name")
        location = geolocator.geocode(address)
        print(location.address)
        print((location.latitude, location.longitude))
        office_coords.append(
            {
                'city': address,
                'x': str(location.longitude),
                'y': str(location.latitude)
                
            }
        )
    json.dump(office_coords,file, indent=4,ensure_ascii=False)
