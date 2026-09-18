import os
import asyncio

from telethon import TelegramClient, events
from telethon.sessions import StringSession

API_ID = int(os.environ["TG_API_ID"])
API_HASH = os.environ["TG_API_HASH"]
SESSION = os.environ["TG_SESSION"]

BACK_BOT_TOKEN = os.environ["BACK_BOT_TOKEN"]
YOUR_TELEGRAM_ID = int(os.environ["YOUR_TELEGRAM_ID"])

# Реальний Front-account
front = TelegramClient(
    StringSession(SESSION),
    API_ID,
    API_HASH
)

# Back Bot
back = TelegramClient(
    "back_bot",
    API_ID,
    API_HASH
)


async def main():
    await front.start()

    await back.start(
        bot_token=BACK_BOT_TOKEN
    )

    print("Front account connected")
    print("Back bot connected")

    await asyncio.gather(
        front.run_until_disconnected(),
        back.run_until_disconnected()
    )


asyncio.run(main())
