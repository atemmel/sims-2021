import csv
cities = []

with open("../datasets/swedish_cities.csv", "r", encoding="UTF-8") as file:
   cities =  file.readlines()
   cities = [city.rstrip() for city in cities]
   
with open("swedish_cities.csv", "w", encoding="UTF-8", newline='') as file:
    writer = csv.writer(file,delimiter=',',quoting= csv.QUOTE_NONE)

    for city in cities:       
        writer.writerow(["SwedishCities",city])

