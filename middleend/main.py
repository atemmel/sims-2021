#!/usr/bin/env python

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import AssistantV2
from ibm_watson import ApiException
import json

def read_auth(string):
    with open(string) as file:
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

try:
    auth = read_auth("./auth.json");

    authenticator = IAMAuthenticator(auth["authenticator"])
    assistant = AssistantV2(
        version='2021-06-14',
        authenticator=authenticator
    )

    assistant.set_service_url(auth["service_url"])


    response = assistant.create_session(
        assistant_id = auth["assistant_id"]
    ).get_result()

    print(json.dumps(response, indent=2))

    session_id = response["session_id"]

    response = send_message(assistant, session_id, auth, "I like purple")
    print(json.dumps(response, indent=2))

    response = assistant.delete_session(
        assistant_id = auth["assistant_id"],
        session_id = session_id,
    ).get_result()

    print(json.dumps(response, indent=2))

except ApiException as ex:
    print("Method failed with status code", str(ex.code) , ":" , ex.message)
