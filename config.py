import os

flask_app_config = {
    "debug": os.environ.get("FLUSK_DEBUG_OPTION", True),
    "host": os.environ.get("FLASK_HOST", None),
    "port": os.environ.get("FLASK_PORT", 443),
    "ssl_context": os.environ.get("SSL_CONTEX","adhoc")
}


CLIENT_ID = os.environ.get("DB_HOST", "placeholder")
SECRET = os.environ.get("DB_HOST", "placeholder")
BROADCASTER_ID = os.environ.get("DB_HOST", 0)
DOMINIO = os.environ.get("DB_HOST", "placeholder")
REDIRECT_URI_AUTHORIZATION_CODE = os.environ.get("DB_HOST", DOMINIO + "/authorization_code_interceptor")
REDIRECT_URI_CHANNEL_POINT_NOTIFICATION = os.environ.get("DB_HOST", DOMINIO + "/channel_point_notification")

NGROK_AUTH_TOKEN = os.environ.get("DB_HOST", "placeholder")


print(flask_app_config)

print("CLIENT_ID: ","CLIENT_ID")
print("SECRET: ","SECRET")
print("BROADCASTER_ID: ","BROADCASTER_ID")
print("DOMINIO: ","DOMINIO")
print("REDIRECT_URI_AUTHORIZATION_CODE: ","REDIRECT_URI_AUTHORIZATION_CODE")
print("REDIRECT_URI_CHANNEL_POINT_NOTIFICATION: ","REDIRECT_URI_CHANNEL_POINT_NOTIFICATION")
print("NGROK_AUTH_TOKEN: ","NGROK_AUTH_TOKEN")
