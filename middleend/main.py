#!/usr/bin/env python
import argparse
import eventlet
from ibm_watson import ApiException
import json
import socketio
from time import sleep

from backend_connection import BackendConnection
import common

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)
articles = {}
backend_connection = None

def do_repl():
    client = "cli"
    backend_connection.connect_client(client)
    session = backend_connection.get_session(client)
    while True:
        try:
            message = input(">> ")
            response = backend_connection.send_message(message, session)
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

def find_offices(offices,city):
    foundOffices= []
    for office in offices:
        if office["visit-adress"]["city"] == city:
            foundOffices.append(office)
    print(foundOffices)
    return foundOffices


def load_articles(config):
    return common.read_json_to_dict(config["scraped_articles"])
    
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


def generate_response(response, articles):
    entities = response["output"]["entities"]
    # If the response has entities
    if len(entities) > 0:
        tags = [entity["value"] for entity in list(filter(lambda entity: entity["entity"] == "ArticleTag", entities))]
        return get_articles_and_urls(response, articles, tags)
    return {
        "text": response["output"]["generic"][0]["text"],
        "articles": [],
    }

def get_articles_and_urls(response, articles, tags):
    message = response["output"]["generic"][0]["text"]
    category = response["output"]["entities"][0]["value"]
    articles_in_category = find_article_category(articles,category)
    if len(articles_in_category) > 0:
        string_to_replace = "{" + category + "}"
        message = message.replace(string_to_replace, '')
        selected_articles = articles_in_category[:3]
        selected_articles_response = []

        for article in selected_articles:
            temp_article = {
                'title': article["title"],
                'url': article["url"]
            }
            selected_articles_response.append(temp_article)

        res = {
            'text': message,
            'articles': selected_articles_response
        }
        return res
    else:
        articles_with_tag = find_articles_with_tags(articles, tags)
        if len(articles_with_tag) > 3:
            articles_with_tag = articles_with_tag[:3]
        return {
            "text": message,
            "articles": articles_with_tag,
        }

@sio.on('connect')
def connect(sid, _):
    print('connecting', sid)
    # Returns true/false, should perhaps be handled(?)
    backend_connection.connect_client(sid)

    backend_connection.clients_lock.acquire()
    session_id = backend_connection.clients_session[sid]
    backend_connection.clients_lock.release()

    response = backend_connection.send_message("", session_id)
    if not backend_connection.send_message_succeeded(response):
        print("Could not send message:")
        print(json.dumps(response, indent=2))
    else:
        response = {"text": response["output"]["generic"][0]["text"]}

    sio.emit('event', {'response': response}, room=sid)
    print(response)

@sio.on('disconnect')
def disconnect(sid):
    print('disconnect', sid)
    backend_connection.disconnect_client(sid)

@sio.on('event')
def message(sid, data):
    session_id = backend_connection.get_session(sid)

    response = backend_connection.send_message(data, session_id)
    print(response)
    if not backend_connection.send_message_succeeded(response):
        print("Could not send message:")
        print(json.dumps(response, indent=2))
    else:
        response = generate_response(response, articles)
        sio.emit('event', {'response': response}, room=sid)
        print(response)


def main():
    global articles, backend_connection

    parser = argparse.ArgumentParser(description="Run middleend")
    parser.add_argument("--cli", action="store_true", help="Run in cli-mode")
    args = parser.parse_args()

    config = common.read_json_to_dict("./config.json")
    articles = load_articles(config)

    # Commenting this out temporary
    # offices = load_offices(config)

    
    backend_connection = BackendConnection("./auth.json")
    try:
        if args.cli:
            do_repl()
        else:
            eventlet.wsgi.server(eventlet.listen(('', config["port"])), app)
            # Cleanup
            sleep(1.0)

        backend_connection.clean_up_all_sessions()
    except ApiException as ex:
        print("Method failed with status code", str(ex.code) , ":" , ex.message)

if __name__ == "__main__":
    main()
