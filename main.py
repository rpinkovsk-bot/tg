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

# Зв’язок:
# back_message_id -> front_message_id
message_map = {}


@front.on(events.NewMessage(incoming=True))
async def front_handler(event):
    # Поки працюємо тільки з твоїм основним Telegram
    if event.sender_id != YOUR_TELEGRAM_ID:
        return

    # Пересилаємо повідомлення в Back Bot
    sent = await back.send_message(
        YOUR_TELEGRAM_ID,
        event.message
    )

    message_map[sent.id] = event.message.id

    print(
        f"Front -> Back: "
        f"{event.message.id} -> {sent.id}"
    )


@back.on(events.NewMessage(incoming=True))
async def back_handler(event):
    # Ігноруємо всіх, крім тебе
    if event.sender_id != YOUR_TELEGRAM_ID:
        return

    reply_to = event.message.reply_to_msg_id

    if reply_to and reply_to in message_map:
        front_message_id = message_map[reply_to]

        await front.send_message(
            YOUR_TELEGRAM_ID,
            event.message,
            reply_to=front_message_id
        )

        print(
            f"Back reply -> Front: "
            f"{reply_to} -> {front_message_id}"
        )

    else:
        # Якщо в Back пишеш без Reply —
        # просто нове повідомлення у Front
        await front.send_message(
            YOUR_TELEGRAM_ID,
            event.message
        )

        print("Back -> Front new message")


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
