import json


def kind_of_json_to_json(input_file, output_file):
    with open(input_file, "r", encoding="UTF-8") as file:
        json_file = json.loads(file.read())
        better_json = []
        for json_row in json_file:
            json_row = json.loads(json_row)
            better_json.append(json_row)

    with open(output_file, "w", encoding="utf8") as outfile:
        json.dump(better_json, outfile, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


kind_of_json_to_json("../datasets/cinode-data/CompanyUser.json", "../datasets/cinode-data/cinode-data/BetterCompanyUser.json")
kind_of_json_to_json("../datasets/cinode-data/CompanyUserSkills.json", "../datasets/cinode-data/cinode-data/BetterCompanyUserSkills.json")