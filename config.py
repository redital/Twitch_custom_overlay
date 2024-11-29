import os

flask_app_config = {
    "debug": os.environ.get("FLUSK_DEBUG_OPTION", True),
    "host": os.environ.get("FLASK_HOST", "0.0.0.0"),
    "port": os.environ.get("FLASK_PORT", 5000),
}


CLIENT_ID = os.environ.get("CLIENT_ID", "placeholder")
SECRET = os.environ.get("SECRET", "placeholder")
BROADCASTER_ID = os.environ.get("BROADCASTER_ID", 0)
DOMINIO = "https://" + os.environ.get("DOMINIO", "placeholder")
REDIRECT_URI_AUTHORIZATION_CODE = os.environ.get("REDIRECT_URI_AUTHORIZATION_CODE", DOMINIO + "/authorization_code_interceptor")
REDIRECT_URI_CHANNEL_POINT_NOTIFICATION = os.environ.get("REDIRECT_URI_CHANNEL_POINT_NOTIFICATION", DOMINIO + "/channel_point_notification")

NGROK_AUTH_TOKEN = os.environ.get("NGROK_AUTH_TOKEN", "placeholder")


print(flask_app_config)

print("CLIENT_ID: ",CLIENT_ID)
print("SECRET: ",SECRET)
print("BROADCASTER_ID: ",BROADCASTER_ID)
print("DOMINIO: ",DOMINIO)
print("REDIRECT_URI_AUTHORIZATION_CODE: ",REDIRECT_URI_AUTHORIZATION_CODE)
print("REDIRECT_URI_CHANNEL_POINT_NOTIFICATION: ",REDIRECT_URI_CHANNEL_POINT_NOTIFICATION)
print("NGROK_AUTH_TOKEN: ",NGROK_AUTH_TOKEN)
