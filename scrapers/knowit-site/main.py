#!/usr/bin/env python

import json
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

targets = [
    ["https://www.knowit.eu", "/our-clients/", "knowit-site-eu.json"],
    ["https://www.knowit.se", "/kunder/", "knowit-site-se.json"],
]

company_fields_from_scraper = [
    ["bank-finans-forsakring", "energi", "handel-tjanster", "halsa", "industri",
     "media-utbildning", "offentlig-sektor", "telekom"],

    ["banking-finance--insurance", "energy", "retail--services",
     "life-science--medical", "industry", "media-education", "public-sector", "telecom"]
]

company_fields = [
    ["Bank, finans & försäkring", "Energi", "Handel & tjänster","Hälsa och livsstil", "Industri",
     "Media & utbildning", "Offentlig sektor", "Telekom"],

    ["Banking, finance & insurance", "Energy", "Retail & services", "Life science & medical",
     "Manufacturing industry", "Media & education", "Public sector", "Telecom"]
]

PAGE_ATTRIBUTE = "?page="
OUTPUT_TRANSLATED_FILENAME = 'knowit-site-se-translated-to-en.json'

def extract_company_field(company_field_from_url):

    # Swedish
    if company_field_from_url in company_fields_from_scraper[0]:
        index = company_fields_from_scraper[0].index(company_field_from_url)
        return company_fields[0][index]

    # English
    if company_field_from_url in company_fields_from_scraper[1]:
        index = company_fields_from_scraper[1].index(company_field_from_url)
        return company_fields[1][index]

def build_article(element, base_url):
    article = dict()
    segregated = element["href"].split("/")
    article["url"] = base_url + element["href"]

    # article["company-field"] = segregated[2].replace("-", " ")
    article["company-field"] = extract_company_field(segregated[2])

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

def translate_company_field(company_field):
    if company_field in company_fields[0]:
        index = company_fields[0].index(company_field)
        return company_fields[1][index]

def translate(text):
    return GoogleTranslator(source='auto', target='en').translate(text)

def translate_articles(input_file_name, output_file_name):
    with open(input_file_name, 'r', encoding="utf8") as input_file, \
         open(output_file_name, 'w', encoding="utf8") as outfile:

        articles = json.load(input_file)
        for article in articles:
            article['company-field'] = translate_company_field(article['company-field'])
            article['content'] = translate(article['content'])
            article['title'] = translate(article['title'])
        json.dump(articles, outfile, ensure_ascii=False, sort_keys=True, indent=4)

for target in targets:
    base_url = target[0]
    full_url = base_url + target[1]
    file_name = target[2]
    pipeline(full_url, base_url, file_name)

translate_articles(targets[1][2], OUTPUT_TRANSLATED_FILENAME)