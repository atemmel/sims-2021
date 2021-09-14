#!/usr/bin/env python

import json
import requests
from bs4 import BeautifulSoup

URL = "https://www.knowit.eu/our-clients/"

def build_article(element):
    article = dict()
    segregated = element["href"].split("/")
    article["company-field"] = segregated[2]
    article["company-name"] = segregated[3]
    element = element.find("div", class_="content-block_textblock editorial")
    title_element = element.find("h2", class_="content-block_heading")
    article["title"] = title_element.text
    content_element = element.find("div", class_="content-block_text")
    article["content"] = content_element.text.strip()
    return article

def find_all_articles():
    return soup.find_all("a", class_="content-block")

page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
results = find_all_articles()
articles = list()

for result in results:
    articles.append(build_article(result))

with open("knowit-site.json", "w") as outfile:
    json.dump(articles, outfile)
