from telegram import Bot

from telegram_bot.utils.token_parser import get_bot_token
from telegram_bot.utils import db_utils
import app_strings


def send_telegram_message(chat_id: str, message: str):
    bot = Bot(token=get_bot_token())
    bot.send_message(chat_id, message)


def send_email(email: str, username: str, message: str):
    pass


def get_train_info_message(train, date_fmt, conn) -> str:
    return f"Treno numero: {train.code};\n" \
        f"Parte da: {db_utils.get_station_from_code(train.depart_stat, conn).name};\n" \
        f"Tua partenza: {date_fmt}\n" \
        f"Carrozza: {train.coach or 'Assente'}\n" \
        f"Posto: {train.seat or 'Assente'}\n"

