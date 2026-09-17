import os
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_id = int(os.environ["TG_API_ID"])
api_hash = os.environ["TG_API_HASH"]
phone = os.environ["FRONT_PHONE"]

with TelegramClient(StringSession(), api_id, api_hash) as client:
    client.start(phone=phone)

    print("\nSESSION STRING:")
    print(client.session.save())
