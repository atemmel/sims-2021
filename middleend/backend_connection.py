from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import ApiException, AssistantV2
from threading import Lock

import common

class BackendConnection:
    assistant = None
    auth = {}
    clients_session = {}
    clients_lock = Lock()

    def __init__(self, auth_path):
        self.auth = common.read_json_to_dict(auth_path)
        authenticator = IAMAuthenticator(self.auth["authenticator"])
        self.assistant = AssistantV2(
            version='2021-06-14',
            authenticator=authenticator
        )

        self.assistant.set_service_url(self.auth["service_url"])

    def connect_client(self, client):
        response = self.create_session()
        if not self.create_session_succeeded(response):
            return False
        self.clients_lock.acquire()
        self.clients_session[client] = response["session_id"]
        self.clients_lock.release()
        return True

    def disconnect_client(self, client):
        self.clients_lock.acquire()
        self.delete_session(self.clients_session[client])
        del self.clients_session[client]
        self.clients_lock.release()

    def create_session(self):
        response = self.assistant.create_session(
            assistant_id = self.auth["assistant_id"]
        ).get_result()

        return response

    def delete_session(self, session_id):
        self.assistant.delete_session(
            assistant_id = self.auth["assistant_id"],
            session_id = session_id,
        )

    def clean_up_all_sessions(self):
        for session in self.clients_session:
            self.delete_session(session)

    def create_session_succeeded(self, response):
        return "session_id" in response.keys()

    def send_message(self, message, session_id):
        print("Sending message:", message)
        response = self.assistant.message(
            assistant_id = self.auth["assistant_id"],
            session_id = session_id,
            input = {
                'message_type': 'text',
                'text': message,
            }
        ).get_result()

        return response

    def send_message_succeeded(self, response):
        return "output" in response.keys()
