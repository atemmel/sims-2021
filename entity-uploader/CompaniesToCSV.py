import csv
import json

companies_csv = []

def companies_to_csv(input_name, output_name):
    with open(input_name, 'r', encoding="utf8") as file, \
            open(output_name, 'w', encoding="utf8", newline='') as outfile:
        companies_json = json.loads(file.read())
        writer = csv.writer(outfile, delimiter=',', quoting=csv.QUOTE_ALL)
        for company in companies_json:
            writer.writerow(["CompanyName", company["name"]])

companies_to_csv("../datasets/companies.json", "companies.csv")
