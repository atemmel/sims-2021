#!/usr/bin/env python
import eventlet
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import ApiException, AssistantV2
import json
import socketio
from threading import Lock
from time import sleep

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)
articles, assistant, auth = None, None, None
clients_session = {}
clients_lock = Lock()

def do_repl(articles, assistant, session_id, auth):
    while True:
        try:
            message = input(">> ")
            response = send_message(assistant, session_id, auth, message)
            if not send_message_succeeded(response):
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

def connect_client(auth, assistant, client):
    response = create_session(auth, assistant)
    if not create_session_succeeded(response):
        return False
    clients_lock.acquire()
    clients_session[client] = response["session_id"]
    clients_lock.release()
    return True

def disconnect_client(auth, assistant, client):
    clients_lock.acquire()
    delete_session(assistant, clients_session[client], auth)
    del clients_session[client]
    clients_lock.release()

def read_json_to_dict(string):
    with open(string, "r", encoding="UTF-8") as file:
        return json.loads(file.read())

def send_message(assistant, session_id, config, message):
    print("Sending message:", message)
    response = assistant.message(
        assistant_id = config["assistant_id"],
        session_id = session_id,
        input = {
            'message_type': 'text',
            'text': message,
        }
    ).get_result()

    return response

def create_assistant(auth):
    authenticator = IAMAuthenticator(auth["authenticator"])
    assistant = AssistantV2(
        version='2021-06-14',
        authenticator=authenticator
    )

    assistant.set_service_url(auth["service_url"])
    return assistant


def create_session(auth, assistant):
    response = assistant.create_session(
        assistant_id = auth["assistant_id"]
    ).get_result()

    return response

def delete_session(assistant, session_id, auth):
    assistant.delete_session(
        assistant_id = auth["assistant_id"],
        session_id = session_id,
    )

def create_session_succeeded(response):
    return "session_id" in response.keys()

def send_message_succeeded(response):
    return "output" in response.keys()

def extract_message_from_response(response):
    generic = response["output"]["generic"]
    print(generic)

    # Wrapped it in an object to make the frontend happy
    res = {
        'text': [item[item["response_type"]] for item in generic]
    }
    return res

def load_articles(config):
    return read_json_to_dict(config["scraped_articles"])
    
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
    connect_client(auth, assistant, sid)

@sio.on('disconnect')
def disconnect(sid):
    print('disconnect', sid)
    disconnect_client(auth, assistant, sid)

@sio.on('event')
def message(sid, data):
    clients_lock.acquire()
    session_id = clients_session[sid]
    clients_lock.release()

    response = send_message(assistant, session_id, auth, data)
    print(response)
    if not send_message_succeeded(response):
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
    global articles, assistant, auth
    port = 80
    auth = read_json_to_dict("./auth.json")
    config = read_json_to_dict("./config.json")
    articles = load_articles(config)
    
    assistant = create_assistant(auth)
    try:
        eventlet.wsgi.server(eventlet.listen(('', port)), app)

        # Cleanup
        sleep(1)
        for session in clients_session:
            delete_session(assistant, session, auth)
    except ApiException as ex:
        print("Method failed with status code", str(ex.code) , ":" , ex.message)

if __name__ == "__main__":
    main()
