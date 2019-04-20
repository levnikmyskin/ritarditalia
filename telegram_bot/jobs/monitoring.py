import logging

import MySQLdb
import app_strings
import re
import itertools

from telegram_bot import stickers
from telegram_bot.utils.date_helper import *
from telegram_bot.utils.language_utils import set_language
from telegram_bot.utils.trains_api import get_train_status, timestamp_to_italy_datetime
from telegram_bot.utils.notifications import send_telegram_message
from telegram_bot.utils.db_utils import get_user, get_station_from_code, get_trains_to_monitor
from telegram_bot.utils.structs import Train, TrainStatus
from datetime import datetime
from collections import deque
from config import *


def consume(iterator, n=None):
    """
    Advance the iterator n-steps ahead. If n is None, consume entirely.
    Check https://docs.python.org/3.7/library/itertools.html#itertools-recipes
    """
    # Use functions that consume iterators at C speed.
    if n is None:
        # feed the entire iterator into a zero-length deque
        deque(iterator, maxlen=0)
    else:
        # advance to the empty slice starting at position n
        next(itertools.islice(iterator, n, n), None)


def _get_interval_days(start: str, end: str) -> iter:
    """
    Get the interval between the start and end days (exclusive), each formatted as a three-chars long string.
    We first create an infinite cycle with itertools.cycle, then we consume it until we reach the 'start'
    day and finally we take all days from there to the 'end' day.
    We don't need to include the start and end day in the list since we already have them
    """
    start_index = interval_days.index(start)
    day_cycle = itertools.cycle(interval_days)
    consume(day_cycle, start_index + 1)
    return itertools.takewhile(lambda d: d != end, day_cycle)


def _is_in_day_interval(days, interval, weekday) -> bool:
    """
    Check if weekday (as a number) is either in the interval or in the days lists.
    Interval list should be as ["lun-mer", "gio-dom", ...]
    Days list should be as ["lun", "mar", "mer"]
    """
    inter_days = list()
    if interval:
        for inter in interval:
            inter = inter.split("-")
            inter_days = itertools.chain(_get_interval_days(inter[0], inter[1]), inter_days, inter)

    # Check that any of the items in the iterables matches today (the 'd and' is needed because we might get '' from
    # the split function used above)
    return any(map(lambda d: d and days_mapping[d] == weekday, itertools.chain(inter_days, days)))


def _prepare_days_and_interval(check_interval):
    days = list()
    interval = list()
    if check_interval:
        date_list = check_interval.split(",")
        for date in date_list:
            if len(date) > 3:
                interval.append(date)
            elif len(date) > 0:
                days.append(date)
    return days, interval


def _is_daily_update_to_be_sent(train):
    # We need to check if train depart.time is after current time, if check daily was enabled and if we're in the
    # day interval specified by the user. To do this, we get the "days" and "interval" groups from the regex
    # and we return true
    now_date = datetime.now()
    is_in_day_interval = True
    if train.check_interval:
        days, interval = _prepare_days_and_interval(train.check_interval)
        is_in_day_interval = _is_in_day_interval(days, interval, now_date.weekday())

    return train.depart_date.time() > now_date.time() and train.check_daily and is_in_day_interval


def get_status_message(status: dict, train: Train, conn: MySQLdb.Connection, lang=None) -> (str, TrainStatus):
    if lang:
        set_language(lang)
    if status.get('error', False):
        return status["error"]["message"], TrainStatus.ERROR
    elif status.get('oraUltimoRilevamento') is not None:
        delay = status['ritardo']
        if delay > 0:
            message = _(app_strings.train_delayed)
        else:
            message = _(app_strings.train_on_time)

        depart_station = get_station_from_code(train.depart_stat, conn)
        date = timestamp_to_italy_datetime(status['oraUltimoRilevamento']).strftime("%d/%m/%Y %H:%M")
        actual_last_stop = filter(lambda s: s['stazione'] == status['stazioneUltimoRilevamento'], status["fermate"])
        last_stop_status = f"{status['stazioneUltimoRilevamento']}"
        try:
            actual_last_stop = next(actual_last_stop)
            if actual_last_stop['partenzaReale'] is not None:
                last_stop_status = f"{_(app_strings.departed_from)}{status['stazioneUltimoRilevamento']}"
            elif actual_last_stop['arrivoReale'] is not None:
                last_stop_status = f"{_(app_strings.arrived_to)}{status['stazioneUltimoRilevamento']}"
        except StopIteration:
            pass
        return f"{message}\nTreno numero: {train.code};\n" \
                   f"Partito da: {depart_station.name};\n" \
                   f"Ritardo/Anticipo: {delay} minuti;\n" \
                   f"Ultimo rilevamento: {date};\n" \
                   f"Ultima stazione: {last_stop_status}", TrainStatus.AVAILABLE
    else:
        return _(app_strings.train_status_not_available), TrainStatus.NOT_AVAILABLE


def send_status_info(chat_id: str, message: str, conn: MySQLdb.Connection):
    send_telegram_message(chat_id, message)


def run(bot, job):
    conn = MySQLdb.connect(passwd=DB_PASSWORD, user=DB_USER, host=DB_HOST, db=DB_NAME)
    to_monitor = get_trains_to_monitor(conn)
    for train in to_monitor:
        try:
            if train.depart_date > datetime.now() or _is_daily_update_to_be_sent(train):
                user = get_user(conn, chat_id=train.user)
                status = get_train_status(train.depart_stat, train.code)
                message, status = get_status_message(status, train, conn, lang=user.lang)
                if status == TrainStatus.AVAILABLE:
                    send_status_info(train.user, message, conn)
        except Exception as e:
            logging.error(e)
    conn.close()


if __name__ == '__main__':
    run(None, None)
