import os
from google.cloud import secretmanager

def get_secret(secret):
    secret = os.getenv(secret)
    if secret == None:
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/discord-bot-38/secrets/{secret}/versions/latest"
        response = client.access_secret_version(name=name)
        secret = response.payload.data.decode('UTF-8')
    return secret