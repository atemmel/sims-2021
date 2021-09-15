#!/usr/bin/env python

import json
import requests
from bs4 import BeautifulSoup

targets = [
    ["https://www.knowit.eu", "/our-clients/", "knowit-site-eu.json"],
    ["https://www.knowit.se", "/kunder/", "knowit-site-se.json"],
]

PAGE_ATTRIBUTE = "?page="

def build_article(element, base_url):
    article = dict()
    segregated = element["href"].split("/")
    article["url"] = base_url + element["href"]
    article["company-field"] = segregated[2].replace("-", " ")
    article["company-name"] = segregated[3].replace("-", " ")
    element = element.find("div", class_="content-block_textblock editorial")
    title_element = element.find("h2", class_="content-block_heading")
    article["title"] = title_element.get_text()
    content_element = element.find("div", class_="content-block_text")
    article["content"] = content_element.get_text().strip()
    return article

def find_all_articles(soup):
    return soup.find_all("a", class_="content-block")

def request_until_out_of_pages(full_url, base_url):
    all_articles = list()
    page_number = 1
    while True:
        page = requests.get(full_url + PAGE_ATTRIBUTE + str(page_number))
        soup = BeautifulSoup(page.content, "html.parser")
        html = find_all_articles(soup)
        if len(html) == 0:
            return all_articles
        for element in html:
            all_articles.append(build_article(element, base_url))
        page_number += 1

def pipeline(target_full_url, target_base_url, file_name):
    articles = request_until_out_of_pages(target_full_url, target_base_url)
    with open(file_name, "w", encoding="utf8") as outfile:
        json.dump(articles, outfile, ensure_ascii=False, sort_keys=True, indent=4)

for target in targets:
    base_url = target[0]
    full_url = base_url + target[1]
    file_name = target[2]
    pipeline(full_url, base_url, file_name)
