# import ngrok python sdk
import ngrok
import time
from parameti_segreti import NGROK_AUTH_TOKEN, NGROK_STATIC_DOMAIN

# Establish connectivity
listener = ngrok.forward(5000,authtoken=NGROK_AUTH_TOKEN,domain=NGROK_STATIC_DOMAIN)

# Output ngrok url to console
print(f"Ingress established at {listener.url()}")

# Keep the listener alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Closing listener")