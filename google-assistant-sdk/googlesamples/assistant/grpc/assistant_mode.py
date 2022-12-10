import click
import os
import json
import google.auth.transport.grpc
import google.auth.transport.requests
import google.oauth2.credentials
from pushtotalk import SampleAssistant
try:
    from . import (
        assistant_helpers,
        audio_helpers,
        browser_helpers,
        device_helpers
    )
except (SystemError, ImportError):
    import assistant_helpers
    import audio_helpers
    import browser_helpers
    import device_helpers

credentials = os.path.join(click.get_app_dir('google-oauthlib-tool'),
                                   'credentials.json')

with open(credentials, 'r') as f:
    credentials = google.oauth2.credentials.Credentials(token=None,
                                                        **json.load(f))
    http_request = google.auth.transport.requests.Request()
    credentials.refresh(http_request)
grpc_channel = google.auth.transport.grpc.secure_authorized_channel(
    credentials, http_request, 'embeddedassistant.googleapis.com')

audio_device = None

audio_sample_rate = audio_helpers.DEFAULT_AUDIO_SAMPLE_RATE
audio_sample_width = audio_helpers.DEFAULT_AUDIO_SAMPLE_WIDTH
audio_block_size = audio_helpers.DEFAULT_AUDIO_DEVICE_BLOCK_SIZE
audio_flush_size = audio_helpers.DEFAULT_AUDIO_DEVICE_FLUSH_SIZE
audio_iter_size = audio_helpers.DEFAULT_AUDIO_ITER_SIZE

audio_source = audio_device = (
    audio_device or audio_helpers.SoundDeviceStream(
        sample_rate=audio_sample_rate,
        sample_width=audio_sample_width,
        block_size=audio_block_size,
        flush_size=audio_flush_size
    )
)

audio_sink = audio_device = (
    audio_device or audio_helpers.SoundDeviceStream(
        sample_rate=audio_sample_rate,
        sample_width=audio_sample_width,
        block_size=audio_block_size,
        flush_size=audio_flush_size
    )
)

conversation_stream = audio_helpers.ConversationStream(
    source=audio_source,
    sink=audio_sink,
    iter_size=audio_iter_size,
    sample_width=audio_sample_width,
)

lang = 'en-US'
device_model_id = 'smart-home-demo-73745-pi-demo-dcqjs5'
device_id  = 'smart-home-demo-73745'
display = False
grpc_deadline = 185
device_handler = device_helpers.DeviceRequestHandler(device_id)
once = True
with SampleAssistant(lang, device_model_id, device_id,
                         conversation_stream, display,
                         grpc_channel, grpc_deadline,
                         device_handler) as assistant:
    wait_for_user_trigger = not once
    while True:
        continue_conversation = assistant.assist()
        wait_for_user_trigger = not continue_conversation
        if once and (not continue_conversation):
            break
