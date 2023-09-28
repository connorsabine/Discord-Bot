import os
from google.cloud import secretmanager

def access_secret_version(secret_id, version_id="latest"):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/discord-bot-38/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode('UTF-8')

def get_secret(name):
    secret = os.getenv(name)
    if secret == None:
        secret = access_secret_version(name)

    return secret