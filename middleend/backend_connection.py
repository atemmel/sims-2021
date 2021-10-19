from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import AssistantV2
from threading import Lock, Thread
import eventlet
import common
import time

class BackendConnection:
    assistant = None
    auth = {}
    clients_session = {}
    clients_lock = Lock()
    timeout_callback = None

    def look_for_timeouts(self):
        while True:
            self.clients_lock.acquire()
            keys = list(self.clients_session.keys())
            self.clients_lock.release()
            now = time.time()
            for key in keys:
                self.clients_lock.acquire()
                value = self.clients_session[key]
                self.clients_lock.release()
                if now - value["timestamp"] >= 60 * 4:
                    self.timeout_callback(key)
                    self.disconnect_client(key)
            time.sleep(2)

    def __init__(self, auth_path, on_timeout):
        self.auth = common.read_json_to_dict(auth_path)
        authenticator = IAMAuthenticator(self.auth["authenticator"])
        self.assistant = AssistantV2(
            version='2021-06-14',
            authenticator=authenticator,
        )

        eventlet.monkey_patch()
        self.timeout_callback = on_timeout
        self.assistant.set_service_url(self.auth["service_url"])

        thread = Thread(target=self.look_for_timeouts)
        thread.start()

    def connect_client(self, client):
        response = self.create_session()
        if not self.create_session_succeeded(response):
            return False
        self.clients_lock.acquire()
        self.clients_session[client] = {
            "session_id": response["session_id"],
            "timestamp": time.time(),
        }
        self.clients_lock.release()
        return True

    def disconnect_client(self, client):
        self.clients_lock.acquire()
        try:
            self.delete_session(self.clients_session[client]["session_id"])
            del self.clients_session[client]
        except KeyError:
            pass
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

    def get_session(self, client):
        self.clients_lock.acquire()
        session_id = ""
        try:
            session_id = self.clients_session[client]["session_id"]
        except KeyError as e:
            self.clients_lock.release()
            raise e
        self.clients_lock.release()
        return session_id

    def clean_up_all_sessions(self):
        for session in self.clients_session.values():
            self.delete_session(session)

    def create_session_succeeded(self, response):
        return "session_id" in response.keys()

    def send_message(self, message, session_id, sid):
        self.clients_lock.acquire()
        self.clients_session[sid]["timestamp"] = time.time()
        self.clients_lock.release()
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
