import MySQLdb
import app_strings
from telegram_bot.utils.language_utils import set_language
from telegram_bot.utils.trains_api import get_train_status, timestamp_to_italy_datetime
from telegram_bot.utils.notifications import send_telegram_message
from telegram_bot.utils.db_utils import get_user, get_station_from_code, get_trains_to_monitor
from telegram_bot.utils.structs import Train
from datetime import datetime
from config import *


def get_status_message(status: dict, train: Train, conn: MySQLdb.Connection, lang=None) -> (str, bool):
    if lang:
        set_language(lang)
    if status.get('error', False):
        return status["error"]["message"], False
    elif status.get('oraUltimoRilevamento') is not None:
        delay = status['ritardo']
        if delay > 0:
            message = _(app_strings.train_delayed.format(delay))
        else:
            message = _(app_strings.train_on_time)

        depart_station = get_station_from_code(train.depart_stat, conn)
        date = timestamp_to_italy_datetime(status['oraUltimoRilevamento']).strftime("%d/%m/%Y %H:%M")
        return f"{message}\nTreno numero: {train.code};\n" \
            f"Partito da: {depart_station.name};\n" \
            f"Ritardo/Anticipo: {delay} minuti;\n" \
            f"Ultimo rilevamento: {date};\n" \
            f"Ultima stazione rilevata: {status['stazioneUltimoRilevamento']}", True
    else:
        return _(app_strings.train_status_not_available), False


def send_status_info(chat_id: str, message: str, conn: MySQLdb.Connection):
    send_telegram_message(chat_id, message)


def run(bot, job):
    conn = MySQLdb.connect(passwd=DB_PASSWORD, user=DB_USER, host=DB_HOST, db=DB_NAME)
    to_monitor = get_trains_to_monitor(conn)
    now_time = datetime.now().time()
    
    for train in to_monitor:
        if train.depart_date > datetime.now() or (train.depart_date.time() > now_time and train.check_daily):
            user = get_user(conn, chat_id=train.user)
            status = get_train_status(train.depart_stat, train.code)
            message, status_ok = get_status_message(status, train, conn, lang=user.lang)
            if status_ok:
                send_status_info(train.user, message, conn)
    conn.close()


if __name__ == '__main__':
    run(None, None)
