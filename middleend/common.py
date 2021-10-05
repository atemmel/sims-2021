import json

def read_json_to_dict(string):
    with open(string, "r", encoding="UTF-8") as file:
        return json.loads(file.read())
