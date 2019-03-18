import MySQLdb
import app_strings
import re
import itertools
from telegram_bot.utils.language_utils import set_language
from telegram_bot.utils.trains_api import get_train_status, timestamp_to_italy_datetime
from telegram_bot.utils.notifications import send_telegram_message
from telegram_bot.utils.db_utils import get_user, get_station_from_code, get_trains_to_monitor
from telegram_bot.utils.structs import Train
from datetime import datetime
from collections import deque
from config import *

# Pls send help, close to brainfuck regex that matches strings like:
# lun,mar,mer,ven-dom
# ven-dom,mer,gio,ven
# lun,mar,mer
# ven-dom
# Grouping them in the interval and days groups
interval_pattern = re.compile(r'((?=(\w{3},)*(?P<interval>\w{3}-\w{3})))?(?=(\w{3}-\w{3},)?(?P<days>(\w{3}(([^-]|$),?))*))')
interval_days = ["lun", "mar", "mer", "gio", "ven", "sab", "dom"]
days_mapping = dict(lun=0, mar=1, mer=2, gio=3, ven=4, sab=5, dom=6)


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
    # Get the interval between the start and end days (exclusive), each formatted as a three-chars long string.
    # We first create an infinite cycle with itertools.cycle, then we consume it until we reach the 'start'
    # day and finally we take all days from there to the 'end' day.
    # We don't need to include the start and end day in the list since we already have them
    start_index = interval_days.index(start)
    day_cycle = itertools.cycle(interval_days)
    consume(day_cycle, start_index + 1)
    return itertools.takewhile(lambda d: d != end, day_cycle)


def _is_in_day_interval(days, interval, weekday) -> bool:
    # This and the days list below are needed as empty iterables for chain in None cases
    inter_days = list()
    if days is not None:
        days = days.split(",")
    else:
        days = list()
    if interval is not None:
        interval = interval.split("-")
        inter_days = _get_interval_days(interval[0], interval[1])
    else:
        interval = list()

    # Check that any of the items in the iterables matches today (the 'd and' is needed because we might get '' from
    # the split function used above)
    return any(map(lambda d: d and days_mapping[d] == weekday, itertools.chain(inter_days, days, interval)))


def _is_daily_update_to_be_sent(train):
    # We need to check if train depart. time is after current time, if check daily was enabled and if we're in the
    # day interval specified by the user. To do this, we get the "days" and "interval" groups from the regex
    # and we return true
    now_date = datetime.now()
    is_in_day_interval = True
    if train.check_interval:
        interval = interval_pattern.match(train.check_interval)
        if interval:
            days = interval.group("days")
            interval = interval.group("interval")
            is_in_day_interval = _is_in_day_interval(days, interval, now_date.weekday())

    return train.depart_date.time() > now_date.time() and train.check_daily and is_in_day_interval


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
    for train in to_monitor:
        if train.depart_date > datetime.now() or _is_daily_update_to_be_sent(train):
            user = get_user(conn, chat_id=train.user)
            status = get_train_status(train.depart_stat, train.code)
            message, status_ok = get_status_message(status, train, conn, lang=user.lang)
            if status_ok:
                send_status_info(train.user, message, conn)
    conn.close()


if __name__ == '__main__':
    run(None, None)
