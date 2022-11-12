import os
import json
import click
import google.auth.transport.grpc
import google.auth.transport.requests
import google.oauth2.credentials
from textinput import SampleTextAssistant

credentials = os.path.join(click.get_app_dir('google-oauthlib-tool'),
                                   'credentials.json')
with open(credentials, 'r') as f:
            credentials = google.oauth2.credentials.Credentials(token=None, **json.load(f))
            http_request = google.auth.transport.requests.Request()
            credentials.refresh(http_request)
grpc_channel = google.auth.transport.grpc.secure_authorized_channel(
    credentials, http_request, 'embeddedassistant.googleapis.com')

lang = 'en-US'
device_model_id = 'smart-home-972bf-pi-3yr6fl'
device_id  = 'smart-home-972bf'
display = False
grpc_deadline = 185
with SampleTextAssistant(lang, device_model_id, device_id, display,
                             grpc_channel, grpc_deadline) as assistant:
    assistant.assist(text_query='open all the light')
