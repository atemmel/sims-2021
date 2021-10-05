import csv
import json
cities = []
offices = {}

with open("offices.json", "r", encoding="UTF-8") as file:
   offices = json.loads(file.read())

with open("offices.csv", "w", encoding="UTF-8", newline='') as file:
    writer = csv.writer(file,delimiter=' ',quoting= csv.QUOTE_NONE)

    for office in offices:
        #ex is what's added to the csv file.
        c = "CompanyCity," + office["visit-adress"]["city"]
        #no duplicates
        if not c in cities:
            cities.append(c)

    for city in cities:       
        writer.writerow([city])
