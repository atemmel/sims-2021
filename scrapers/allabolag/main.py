from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import time
import requests
from bs4 import BeautifulSoup

PAGE_ATTRIBUTE = "?page="
target = "https://www.allabolag.se/lista/aktiebolag/24"

driver = webdriver.Chrome('./chromedriver')

def build_article(element):
    company = dict()
    company["company-field"] = element.find("dd").find_next_sibling("dd").get_text()
    element = element.find("div", class_="tw-flex")
    company["name"] = element.find("a").get_text()
    company["city"] = element.find_next_sibling("div", class_="search-resuladeritem__subtitle").get_text()
    return company

def find_all_companies(soup):
    #return soup.find_all("div", class_="search-results__item tw-flex-1")
    return soup.find_all("div", class_="search-results__item tw-flex-1")


def request_until_out_of_pages(url):
    all_companies = list()
    page_number = 1
    while True:
        page = requests.get(url + PAGE_ATTRIBUTE + str(page_number))
        soup = BeautifulSoup(page.content, "html.parser")
        html = find_all_companies(soup)
        if len(html) == 0:
            return all_companies
        for element in html:
            all_companies.append(build_article(element))
        page_number += 1

def request_until_out_of_pages_test(url):
    all_companies = list()
    page_number = 1

    while True:
        driver.get(url + PAGE_ATTRIBUTE + str(page_number))
        html = driver.page_source

        soup = BeautifulSoup(html, "html.parser")
        html_soup = find_all_companies(soup)
        if len(html_soup) == 0:
            return all_companies
        for element in html_soup:
            all_companies.append(build_article(element))
        page_number += 1

companies = request_until_out_of_pages_test(target)

with open("../datasets/companies.json", "w", encoding="utf8") as outfile:
    json.dump(companies, outfile, ensure_ascii=False, sort_keys=True, indent=4)