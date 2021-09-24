#!/usr/bin/env python

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import AssistantV2
from ibm_watson import ApiException
import json

def read_json_to_dict(string):
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
    return [item[item["response_type"]] for item in generic]

def main():
    auth = read_json_to_dict("./auth.json")

    try:
        assistant, response = create_session(auth)
        if not create_session_succeeded(response):
            print("Could not create session:")
            print(json.dumps(response, indent=2))
            return 1

        session_id = response["session_id"]

        while True:
            try:
                message = input(">> ")
                response = send_message(assistant, session_id, auth, message)
                if not send_message_succeeded(response):
                    print("Could not send message:")
                    print(json.dumps(response, indent=2))
                else:
                    print(extract_message_from_response(response))

            except (KeyboardInterrupt, EOFError):
                print("\nExiting...")
                break

        delete_session(assistant, session_id, auth)
    except ApiException as ex:
        print("Method failed with status code", str(ex.code) , ":" , ex.message)

if __name__ == "__main__":
    main()
