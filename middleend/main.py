#!/usr/bin/env python
import eventlet
import socketio

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import AssistantV2
from ibm_watson import ApiException
import json

from requests.models import ContentDecodingError
sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)
articles, assistant, session_id, auth = None, None, None, None

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

def create_session(auth):
    authenticator = IAMAuthenticator(auth["authenticator"])
    assistant = AssistantV2(
        version='2021-06-14',
        authenticator=authenticator
    )

    assistant.set_service_url(auth["service_url"])

    response = assistant.create_session(
        assistant_id = auth["assistant_id"]
    ).get_result()

    return assistant, response

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
    return [item[item["response_type"]] for item in generic]

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

@sio.on('connect')
def connect(sid, env):
    print('connecting ', sid)

@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)

@sio.on('event')
def message(sid, data):
    response = send_message(assistant, session_id, auth, data)
    if not send_message_succeeded(response):
        print("Could not send message:")
        print(json.dumps(response, indent=2))
    else:
        if len(response["output"]["entities"]) > 0:
            #Might make a list and store each string in replace_entities depending on what the front gais want.
            response= replace_entities_in_response(response, articles)
        else:
            response = extract_message_from_response(response)
            
        sio.emit('event', {'text': response, 'url': ''}, room=sid)
        print(response)
    

def main():
    global articles,assistant, session_id, auth
    port = 80
    auth = read_json_to_dict("./auth.json")
    config = read_json_to_dict("./config.json")
    articles = load_articles(config)
    
    try:
        assistant, response = create_session(auth)
        if not create_session_succeeded(response):
            print("Could not create session:")
            print(json.dumps(response, indent=2))
            return 1

        session_id = response["session_id"]
        eventlet.wsgi.server(eventlet.listen(('', port)), app)


        delete_session(assistant, session_id, auth)
    except ApiException as ex:
        print("Method failed with status code", str(ex.code) , ":" , ex.message)

if __name__ == "__main__":
    main()
