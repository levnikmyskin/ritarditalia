from telegram import Bot
from telegram_bot.utils.token_parser import get_bot_token


def send_telegram_message(chat_id: str, message: str):
    bot = Bot(token=get_bot_token())
    bot.send_message(chat_id, message)


def send_email(email: str, username: str, message: str):
    pass
