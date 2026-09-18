import os
import asyncio

from telethon import TelegramClient, events
from telethon.sessions import StringSession

API_ID = int(os.environ["TG_API_ID"])
API_HASH = os.environ["TG_API_HASH"]
SESSION = os.environ["TG_SESSION"]

BACK_BOT_TOKEN = os.environ["BACK_BOT_TOKEN"]
YOUR_TELEGRAM_ID = int(os.environ["YOUR_TELEGRAM_ID"])

front = TelegramClient(
    StringSession(SESSION),
    API_ID,
    API_HASH
)

back = TelegramClient(
    "back_bot",
    API_ID,
    API_HASH
)

message_map = {}


@front.on(events.NewMessage(incoming=True))
async def front_handler(event):
    if event.sender_id != YOUR_TELEGRAM_ID:
        return

    sent = await back.send_message(
        YOUR_TELEGRAM_ID,
        event.raw_text
    )

    message_map[sent.id] = event.message.id

    print(
        f"Front -> Back: "
        f"{event.message.id} -> {sent.id}"
    )


@back.on(events.NewMessage(incoming=True))
async def back_handler(event):
    if event.sender_id != YOUR_TELEGRAM_ID:
        return

    try:
        text = event.raw_text
        reply_to = event.message.reply_to_msg_id

        print(
            f"Back received: text={text}, "
            f"reply_to={reply_to}"
        )

        if reply_to and reply_to in message_map:
            front_message_id = message_map[reply_to]

            await front.send_message(
                YOUR_TELEGRAM_ID,
                text,
                reply_to=front_message_id
            )

            print("Back reply -> Front sent")

        else:
            await front.send_message(
                YOUR_TELEGRAM_ID,
                text
            )

            print("Back -> Front sent")

    except Exception as e:
        print("BACK HANDLER ERROR:", repr(e))


async def main():
    await front.start()

    await back.start(
        bot_token=BACK_BOT_TOKEN
    )

    print("Front account connected")
    print("Back bot connected")
    print("Bridge started")

    await asyncio.gather(
        front.run_until_disconnected(),
        back.run_until_disconnected()
    )


asyncio.run(main())
