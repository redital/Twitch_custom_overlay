import hmac
import hashlib
import json
import requests
import config
import datetime
from urllib.parse import urlencode


app_token = {
    "text":None,
    "token_type": None,
    "full_token": None,
    "token_expiration_date": None,
    "token_readable_expiration_date": None
    }

user_token = {
    "text":None,
    "token_type": None,
    "full_token": None,
    "token_expiration_date": None,
    "token_readable_expiration_date": None,
    "refresh_token": None,
    "scope": None
    }

def load_token():
    global user_token
    with open("user_token.ippo","r") as f:
        user_token = json.load(f)
    global app_token
    with open("app_token.ippo","r") as f:
        app_token = json.load(f)

def store_token():
    global user_token
    with open("user_token.ippo","w") as f:
        json.dump(user_token, f)
    global app_token
    with open("app_token.ippo","w") as f:
        json.dump(app_token, f)

load_token()

#Client credentials grant flow
#App Token
def authentication(client_id, client_secret,force = False):
    if validate_auth(app_token) and force!=True:
        print("il token è ancora valido")
        return
    url = 'https://id.twitch.tv/oauth2/token'
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
        }
    params = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials"
        }

    response = requests.post(url, headers=headers,params=params)
    if response.status_code != 200:
        print("ERRORE IN FASE DI AUTENTICAZIONE")
        print(response.text)
        return
    response_body = response.json()

    # for k,v in response_body.items():
    #    print(k,v,sep=": ")

    now = datetime.datetime.now()
    delta = datetime.timedelta(seconds = response_body["expires_in"])
    expires = now + delta

    app_token["text"] = response_body["access_token"]
    app_token["token_type"] = response_body["token_type"]
    app_token["full_token"] = response_body["token_type"].capitalize() + " " + response_body["access_token"]
    app_token["token_expiration_date"] = expires.timestamp()
    app_token["token_readable_expiration_date"] = str(expires)
    store_token()

#Authorization code grant flow
#User Token
def authentication_authorized(client_id, client_secret, redirect_uri, auth_code,force = False):
    if validate_auth(user_token) and force!=True:
        print("il token è ancora valido")
        return
    url = 'https://id.twitch.tv/oauth2/token'
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
        }
    params = {
            "client_id": client_id,
            "client_secret": client_secret,
            "code":auth_code,
            "grant_type": "authorization_code",
            "redirect_uri" : redirect_uri
        }

    response = requests.post(url, headers=headers,params=params)
    if response.status_code != 200:
        print("ERRORE IN FASE DI AUTENTICAZIONE")
        print(response.text)
        return
    
    response_body = response.json()

    #for k,v in response_body.items():
    #    print(k,v,sep=": ")

    now = datetime.datetime.now()
    delta = datetime.timedelta(seconds = response_body["expires_in"])
    expires = now + delta

    user_token["text"] = response_body["access_token"]
    user_token["token_type"] = response_body["token_type"]
    user_token["full_token"] = response_body["token_type"].capitalize() + " " + response_body["access_token"]
    user_token["token_expiration_date"] = expires.timestamp()
    user_token["token_readable_expiration_date"] = str(expires)
    user_token["refresh_token"] = response_body["refresh_token"]
    user_token["scope"] = response_body["scope"]

    store_token()


def refresh_token(client_id, client_secret,force = False):
    if validate_auth(user_token) and force!=True:
        print("il token è ancora valido")
        return
    url = 'https://id.twitch.tv/oauth2/token'
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
        }
    params = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "refresh_token",
            "refresh_token": user_token["refresh_token"]
        }
    
    formatted_params = "?{}".format(urlencode(params))

    response = requests.post(url + formatted_params, headers=headers,params=params)
    if response.status_code != 200:
        print("ERRORE IN FASE DI AUTENTICAZIONE")
        print(response.text)
        return
    response_body = response.json()

    # for k,v in response_body.items():
    #    print(k,v,sep=": ")

    now = datetime.datetime.now()
    delta = datetime.timedelta(seconds = response_body["expires_in"])
    expires = now + delta

    user_token["text"] = response_body["access_token"]
    user_token["token_type"] = response_body["token_type"]
    user_token["full_token"] = response_body["token_type"].capitalize() + " " + response_body["access_token"]
    user_token["token_expiration_date"] = expires.timestamp()
    user_token["token_readable_expiration_date"] = str(expires)
    user_token["refresh_token"] = response_body["refresh_token"]
    user_token["scope"] = response_body["scope"]

    store_token()


def get_auth_url(client_id, redirect_uri,scopes):
    # https://id.twitch.tv/oauth2/authorize?client_id=<your client ID>&redirect_uri=<your registered redirect URI>&response_type=<type>&scope=<space-separated list of scopes>
    #scopes = []
    #for event in events_dict.get_event_types():
    #    event_scopes = events_dict.get_scopes_for_event(event)
    #    for event_scope in event_scopes:
    #        if event_scope.lower() != "public" and event_scope.lower() not in scopes:
    #            scopes.append(event_scope)

    query_params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        #"force_verify": "true",
        "scope": " ".join(scopes)
    }
    formatted_query_params = urlencode(query_params)
    return "https://id.twitch.tv/oauth2/authorize?{}".format(formatted_query_params)


def get_headers(token_tipe = "app"):
    if token_tipe == "user":
        token = user_token
    elif token_tipe == "app":
        token = app_token
    else:
        print("token_tipe invalido")
        return
    headers = {
        "Client-ID": config.CLIENT_ID,
        "Authorization": token["full_token"]
    }
    return headers


def get_broadcaster_id(username):
    params = {
        "login" : username
    }
    response = send_twitch_request("GET", endpoint="users",params=params)
    return response.json()["data"][0]["id"]
  

def validate_auth(token):
    headers = {
        "Authorization": token["full_token"]
    }
    response = requests.get(url="https://id.twitch.tv/oauth2/validate",headers=headers)
    #response_body = response.json()

    # for k,v in response_body.items():
    #    print(k,v,sep=": ")
    return response.status_code == 200
  
  
def send_twitch_request(method, endpoint, body=None, params=None , headers = None):
    if not headers:
        headers = get_headers()
    url = "https://api.twitch.tv/helix/{}".format(endpoint)
    request_data = {
        "method": method,
        "url": url,
        "headers": headers
    }
    if params:
        request_data["params"] = params
    if body:
        request_data["json"] = body
    response = requests.request(**request_data)
    
    return response


def challenge_response():
    pass

def verify_signature(request):
    hmac_message = request.headers['Twitch-Eventsub-Message-Id'] + request.headers['Twitch-Eventsub-Message-Timestamp'] + request.data.decode()
    message_signature = "sha256=" + hmac.new(str.encode(config.EVENTSUB_SECRET), str.encode(hmac_message), hashlib.sha256).hexdigest()
    if message_signature == request.headers['Twitch-Eventsub-Message-Signature']:
        return True
    return False
