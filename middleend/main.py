#!/usr/bin/env python
import argparse
from collections.abc import Iterable
import eventlet
from ibm_watson import ApiException
import json
import socketio
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from time import sleep

from backend_connection import BackendConnection
import common

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)
articles, offices,number_of_employees, office_coordinates= {}, {}, {}, {}
skill_amounts = []

backend_connection = None

def do_repl():
    client = "cli"
    backend_connection.connect_client(client)
    session = backend_connection.get_session(client)

    while True:
        try:
            message = input(">> ")
            response = backend_connection.send_message(message, session, "cli")
            if not backend_connection.send_message_succeeded(response):
                print("Could not send message:")
            print(json.dumps(generate_response(response, articles), indent=2))


        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break

def extract_message_from_response(response):
    generic = response["output"]["generic"]
    print(generic)

    # Wrapped it in an object to make the frontend happy
    res = {
        'text': [item[item["response_type"]] for item in generic]
    }
    return res

def load_offices(config):
    return common.read_json_to_dict(config["office_location"])

def load_office_coordinates(config):
    return common.read_json_to_dict(config["office_coordinates_location"])

def find_offices(offices,city):
    foundOffices= []
    for office in offices:
        if office["visit-adress"]["city"] == city:
            foundOffices.append(office)
    print(foundOffices)
    return foundOffices

def find_closest_office(location,office_coordinates):
    user_city = location.latitude, location.longitude
    first_city = office_coordinates[0]["y"]+","+office_coordinates[0]["x"]
    dist = geodesic(user_city, first_city).km
    closest_city = office_coordinates[0]["city"]
    
    for i in office_coordinates:
        c = i["y"]+","+i["x"]
        new_distance = geodesic(user_city, c).km
        if new_distance < dist:
            dist = new_distance
            closest_city= i["city"]

    return closest_city

def load_employees(config):
    return common.read_json_to_dict(config["company_users"])

def load_articles(config):
    return common.read_json_to_dict(config["scraped_articles"])

def load_people_with_skills(config):
    return common.read_json_to_dict(config["people_with_skills_location"])

def find_article_category(articles, category):
    found_articles = []
    for article in articles:
        if article["company-field"] == category:
            found_articles.append(article)
    return found_articles
    
def find_articles_with_tags(articles, tags):
    found_articles = []
    for article in articles:
        for tag in tags:
            if tag in article["tags"]:
                found_articles.append(article)
                break
    return found_articles

def find_article_with_company_name(entity, response):
    global articles
    found_articles = []

    for article in articles:
        if entity["value"].lower() == article["company-name"].lower():
            found_articles.append(article)
    return [{
        "text": response["output"]["generic"][0]["text"],
        "articles": found_articles
    }]

def format_office(office):
    return {
        "visitAddress": office["visit-adress"],
        "contactInfo": office["contact-info"],
        "postAddress": {
            "companyName": office["post-adress"]["company-name"],
            "street": office["post-adress"]["street"],
            "zip": office["post-adress"]["zip"],
            "city": office["post-adress"]["city"]
        }
    }

def handle_entity_swedish_city(entity,response):
    global office_coordinates,offices
    geolocator = Nominatim(user_agent="Your_Name") 
    location = geolocator.geocode(entity["value"])
    if location == None:
        print ("Could not find location", entity["value"])
        return [{
            "text":"Could not find location " + entity["value"]+"."
        }]


    closest_office = find_closest_office(location, office_coordinates)
    print(closest_office)
    closest_offices = [format_office(office) for office in offices if office["visit-adress"]["city"] == closest_office]
    return [{
            "text": response["output"]["generic"][0]["text"],
            "offices": closest_offices
        }]
    
def lookup_skill(skill):
    global skill_amounts
    for i, obj in enumerate(skill_amounts):
        if obj["Skill"] == skill:
            return obj["Amount"]
    return -1

def handle_entity_city(entity, response):
    global offices
    found_offices = []
    for office in offices:
        if entity["value"] == office["visit-adress"]["city"]:
            found_offices.append(format_office(office))
    return [{
        "text": response["output"]["generic"][0]["text"],
        "offices": found_offices
    }]

def handle_entity_skill(entity, response):
    found_offices = []

    # Checks if a city was entered in the same message as a skill
    index_of_city = next((i for i, item in enumerate(response["output"]["entities"]) if item['entity'] == 'CompanyCity'), -1)
    if index_of_city == -1:
        skill_amount = lookup_skill(entity["value"])
        text_response = response["output"]["generic"][0]["text"].format(amount=skill_amount)
        return [{
            "text": text_response,
            "offices": found_offices
        }]
    else:
        global offices
        for office in offices:
            if response["output"]["entities"][index_of_city]["value"] == office["visit-adress"]["city"]:
                found_offices.append(format_office(office))
    return [{
        "text": response["output"]["generic"][0]["text"],
        "offices": found_offices
    }]


def generate_response(response, articles):
    entities = response["output"]["entities"]
    intents = response["output"]["intents"]

    relevant_intents = [
        {
            "intent_name": "NumberOfOffices",
            "corresponding_function" : lambda response: [{"text": response["output"]["generic"][0]["text"].replace("{number}", str(len(offices)))}]
        },
        {
            "intent_name": "NumberOfEmployees",
            "corresponding_function" : lambda response: [{"text": response["output"]["generic"][0]["text"].replace("{number}", str(len(number_of_employees)))}]
        }

    ]

    # Add new article-related entities here
    entities_relevant_to_articles = [
        {
            "backend_name": "ArticleTag",
            "dataset_name": "tags"
        },
        {
            "backend_name": "CompanyField",
            "dataset_name": "company-field"
        }
        
    ]

    entities_not_relevant_to_articles = [
        {
            "backend_name": "CompanyCity",
            "corresponding_function": handle_entity_city
        },
        {
            "backend_name": "Skill",
            "corresponding_function": handle_entity_skill
        },
        {
            "backend_name": "CompanyInArticle",
            "corresponding_function": find_article_with_company_name
        },
        {
            "backend_name": "SwedishCities",
            "corresponding_function": handle_entity_swedish_city
        }
    ]

    num_intents = len(intents)
    num_unique_entities = len(set([entity["entity"] for entity in entities]))

    # Incomprehensible
    if num_intents >= 1 and num_unique_entities >= 2 or num_unique_entities >= 3:
        return [{
            "text": "I didn't understand. You can try rephrasing.",
        }]

    print(response)
    if len(intents) > 0:
        intent = intents[0]["intent"]
        print(intent)
        for relevant_intent in relevant_intents:
            if relevant_intent["intent_name"] == intent:
                return relevant_intent["corresponding_function"](response)

    
    # If the response has entities
    if len(entities) > 0:

        for entity in entities:
            entity_name = entity["entity"]
            for relevant_entity in entities_not_relevant_to_articles:
                if relevant_entity["backend_name"] == entity_name:
                    return relevant_entity["corresponding_function"](entity,response)

        article_filter = {"filters": entities_relevant_to_articles}
        for relevant_entity in entities_relevant_to_articles:
            article_filter[relevant_entity["dataset_name"]] = [entity["value"] for entity in list(filter(lambda entity: entity["entity"] == relevant_entity["backend_name"], entities))]

        articles =  get_articles(articles, article_filter)
        if len(articles) > 0:
            return [{
                "text": response["output"]["generic"][0]["text"],
                "articles": articles,
            }, {
                "text": response["output"]["generic"][1]["text"]
            }]
        else:
            return [{
                "text": "Sorry, I could not find any relevant articles to your case",
                "articles": [],
            }]
    return [{
        "text": response["output"]["generic"][0]["text"],
        "articles": [],
    }]

def get_articles(articles, article_filter):
    article_score = [0] * len(articles)

    # Grade articles
    for i in range(len(articles)):
        for filt in article_filter["filters"]:
            filter_property = filt["dataset_name"]
            filter_values = article_filter[filter_property]
            article_property = articles[i][filter_property]

            if isinstance(article_property, Iterable) and not isinstance(article_property, str):
                for filter_value in filter_values:
                    for string in article_property:
                        if string == filter_value:
                            article_score[i] += 1
                            break
            else:
                for filter_value in filter_values:
                    if article_property == filter_value:
                        article_score[i] += 1
                        break

    # Select top scoring articles
    selected_indicies = []
    target_amount = 3
    for i in range(target_amount):
        max_score = max(article_score)
        if max_score <= 0:
            continue
        max_score_index = article_score.index(max_score)
        selected_indicies.append(max_score_index)
        article_score[max_score_index] = -1

    # Whoop whoop
    return [articles[i] for i in selected_indicies]

@sio.on('connect')
def connect(sid, _):
    print('connecting', sid)
    # Returns true/false, should perhaps be handled(?)
    backend_connection.connect_client(sid)

    session_id = backend_connection.get_session(sid)

    response = backend_connection.send_message("", session_id, sid)
    if not backend_connection.send_message_succeeded(response):
        print("Could not send message:")
        print(json.dumps(response, indent=2))
    else:
        response = [{"text": response["output"]["generic"][0]["text"]}]

    sio.emit('event', {'response': response}, room=sid)
    print(response)

@sio.on('disconnect')
def disconnect(sid):
    print('disconnect', sid)
    backend_connection.disconnect_client(sid)

@sio.on('event')
def message(sid, data):
    try:
        session_id = backend_connection.get_session(sid)
    except KeyError:
        backend_connection.connect_client(sid)
        session_id = backend_connection.get_session(sid)
        response = [
            {
                "text": "Alright, I'm back now. What kind of cases are you interested in?",
            }
        ]
        sio.emit('event', {'response': response}, room=sid)
        print(response)
        return

    response = backend_connection.send_message(data, session_id, sid)
    print(response)

    if not backend_connection.send_message_succeeded(response):
        print("Could not send message:")
        print(json.dumps(response, indent=2))
    else:
        response = generate_response(response, articles)
        sio.emit('event', {'response': response}, room=sid)
        print(response)

def on_timeout(sid):
    print(sid, "timed out")
    response = [
        {
            "text": "You haven't spoken with me in a while, so I'll go back to sleep for the time being. Write me something cool to wake me up again!",
        }
    ]
    sio.emit('event', {'response': response}, room=sid)
    print(response)

def main():
    global articles, backend_connection, offices, skill_amounts, number_of_employees, office_coordinates

    parser = argparse.ArgumentParser(description="Run middleend")
    parser.add_argument("--cli", action="store_true", help="Run in cli-mode")
    args = parser.parse_args()

    config = common.read_json_to_dict("./config.json")
    articles = load_articles(config)
    offices = load_offices(config)
    office_coordinates = load_office_coordinates(config)
    skill_amounts = load_people_with_skills(config)
    number_of_employees = load_employees(config)

    backend_connection = BackendConnection("./auth.json", on_timeout)
    try:
        if args.cli:
            do_repl()
        else:
            eventlet.monkey_patch()
            eventlet.wsgi.server(eventlet.listen(('', config["port"])), app)
            # Cleanup
            sleep(1.0)

        backend_connection.clean_up_all_sessions()
    except ApiException as ex:
        print("Method failed with status code", str(ex.code) , ":" , ex.message)

if __name__ == "__main__":
    main()
