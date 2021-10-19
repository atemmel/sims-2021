import re
import csv
import json

companies_csv = []

def companies_to_csv(input_name, output_name):
    with open(input_name, 'r', encoding="utf8") as file, \
            open(output_name, 'w', encoding="utf8", newline='') as outfile:
        companies_json = json.loads(file.read())
        writer = csv.writer(outfile, delimiter=',', quoting=csv.QUOTE_ALL)
        for company in companies_json:
            csv_row = ["CompanyName", company["name"]]
            company_split = company["name"].split()
            if "AB" in company_split:
                csv_row.append(re.sub(r"\bAB\b", "", company["name"]).strip())
            elif "Aktiebolag" in company_split:
                csv_row.append(re.sub(r"\bAktiebolag\b", "", company["name"]).strip())
            elif "Aktiebolaget" in company_split:
                csv_row.append(re.sub(r"\bAktiebolaget\b", "", company["name"]).strip())
            writer.writerow(csv_row)

companies_to_csv("../datasets/companies.json", "companies.csv")
