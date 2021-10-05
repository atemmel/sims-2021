#!/usr/bin/env python
import csv
import json
tags = None

with open("../datasets/tags/tags-p1-2.json", "r", encoding="UTF-8") as file:
   tags = json.loads(file.read())

ENTITY_NAME = "ArticleTag"

with open("tags.csv", "w", encoding="UTF-8", newline='') as file:
    writer = csv.writer(file,delimiter=',',quoting= csv.QUOTE_NONE,escapechar='\\')

    for tag in tags:
        row = [ENTITY_NAME, tag["name"]]
        for synonym in tag["synonyms"]:
            row.append(synonym)
        writer.writerow(row)
