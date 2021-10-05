#!/usr/bin/env python

import json
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

TRANSLATOR_MAX_STRING_SIZE = 5000

def load_json(path):
    with open(path, "r", encoding="UTF-8") as file:
        return json.loads(file.read())

def select_article_contents(soup):
    return soup.find_all("div", class_="content-block_content")

def tags_of_string(string, tags):
    string = string.upper()
    string = string.replace("\n", " ").replace("\t", " ")
    strings = string.split(" ")
    found_tags = []
    for string in strings:
        for tag in tags:
            if tag["name"].upper() == string:
                print(tag["name"], "found")
                found_tags.append(tag["name"])
                continue
            for synonym in tag["synonyms"]:
                if synonym.upper() == string:
                    print(synonym, "found")
                    found_tags.append(tag["name"])
                    break
    return list(set(found_tags))

articles = load_json("../../datasets/knowit-site-se-translated-to-en.json")
# TODO: Change this to final tag file
tags = load_json("../../datasets/tags/tags-p1-2.json")
url_tags_dict = {}

for i in range(len(articles)):
    print("Processing", i, "out of", len(articles))
    article = articles[i]
    url = article["url"]
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    contents = select_article_contents(soup)
    full_str = "".join([content.get_text() for content in contents]).strip()
    if len(full_str) >= TRANSLATOR_MAX_STRING_SIZE:
        full_str = full_str[:TRANSLATOR_MAX_STRING_SIZE - 1]
    translated_str = GoogleTranslator(source='auto', target='en').translate(full_str)
    url_tags_dict[url] = tags_of_string(translated_str, tags)

for i in range(len(articles)):
    url = articles[i]["url"]
    articles[i]["tags"] = url_tags_dict[url]

with open("./tagged-articles.json", "w", encoding="utf8") as file:
    json.dump(articles, file, ensure_ascii=False, sort_keys=True, indent=4)
