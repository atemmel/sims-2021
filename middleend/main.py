#!/usr/bin/env python
import eventlet
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import ApiException, AssistantV2
import socketio
from time import sleep

from backend_connection import BackendConnection
import common

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)
articles = {}
backend_connection = None

def do_repl(articles, assistant, session_id, auth):
    while True:
        try:
            message = input(">> ")
            response = backend_connection.send_message(assistant, session_id, auth, message)
            if not backend_connection.send_message_succeeded(response):
                print("Could not send message:")
                print(json.dumps(response, indent=2))
            else:
                
                if len(response["output"]["entities"]) > 0:
                    print(replace_entities_in_response(response, articles))
                else:
                    print(extract_message_from_response(response))


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
    foundArticles = []
    for article in articles:
        if article["company-field"] == category:
            foundArticles.append(article)
    return foundArticles

def replace_entities_in_response(response, articles):
    message = response["output"]["generic"][0]["text"]
    category = response["output"]["entities"][0]["value"]
    articles_in_category = find_article_category(articles,category)
    selected_articles = articles_in_category[:3]
    string_of_articletext = ""
    for article in selected_articles:
        string_of_articletext += "\n" + article["title"] + "\n" + " (" +  article["url"] + ") \n"

    string_to_replace = "{" + category + "}"
    return message.replace(string_to_replace, string_of_articletext)


def get_articles_and_urls(response, articles):
    message = response["output"]["generic"][0]["text"]
    category = response["output"]["entities"][0]["value"]
    articles_in_category = find_article_category(articles,category)
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
    backend_connection.clients_lock.acquire()
    session_id = backend_connection.clients_session[sid]
    backend_connection.clients_lock.release()

    response = backend_connection.send_message(data, session_id)
    print(response)
    if not backend_connection.send_message_succeeded(response):
        print("Could not send message:")
        print(json.dumps(response, indent=2))
    else:
        if len(response["output"]["entities"]) > 0:
            #Might make a list and store each string in replace_entities depending on what the front gais want.
            response = get_articles_and_urls(response, articles)
        else:
            response = extract_message_from_response(response)

        sio.emit('event', {'response': response}, room=sid)
        print(response)


def main():
    global articles, backend_connection
    config = common.read_json_to_dict("./config.json")
    articles = load_articles(config)

    # Commenting this out temporary
    # offices = load_offices(config)

    
    backend_connection = BackendConnection("./auth.json")
    try:
        eventlet.wsgi.server(eventlet.listen(('', config["port"])), app)

        # Cleanup
        sleep(1)
        backend_connection.clean_up_all_sessions()
    except ApiException as ex:
        print("Method failed with status code", str(ex.code) , ":" , ex.message)

if __name__ == "__main__":
    main()
