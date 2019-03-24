import itertools
import re
from collections import deque
from datetime import datetime
from telegram_bot.utils.exceptions import WrongDateFormatError

# Pls send help, close to brainfuck regex that matches strings like:
# lun,mar,mer,ven-dom
# ven-dom,mer,gio,ven
# lun,mar,mer
# ven-dom
interval_regex = r'((?=(\w{3},)*(\w{3}-\w{3})))?(?=(\w{3}-\w{3},)?((\w{3}(([^-]|$),?))*))'
interval_pattern = re.compile(interval_regex)
interval_split_pattern = re.compile(r'[\s,]')
interval_days = ["lun", "mar", "mer", "gio", "ven", "sab", "dom"]
days_mapping = dict(lun=0, mar=1, mer=2, gio=3, ven=4, sab=5, dom=6)


def parse_date_from_user_message(date: str, hours: str) -> (datetime, str, bool, str):
    """
    Take a date and hours as requested by the monitor command and gives back several results:
    If we get a simple date + hours format, we convert it to a datetime object.
    Else if we get an interval pattern such as lun-ven or sempre we convert the hours to a
    datetime object and we store the interval pattern in the check_interval string, setting
    check_daily to True.
    If check_daily is True, only the hours/minutes of the datetime object should be considered
    """
    check_interval = None
    check_daily = False
    if len(date) >= 30:
        # What the heck did the user just sent? Lol
        raise WrongDateFormatError(f"Date sent from the user was too long, wtf?\nReceived: {date}")
    elif len(date) == 10:
        # The date format we require has length 10
        full_date = datetime.strptime(f"{date} {hours}", "%d/%m/%Y %H:%M")
        full_date_fmt = full_date.strftime("%d/%m/%Y %H:%M")
    else:
        full_date = datetime.strptime(f"{hours}", "%H:%M")
        check_daily = True
        if date != "sempre":
            if not interval_pattern.match(date):
                raise WrongDateFormatError(f"Something's not right with date format, received: {date}")
            check_interval = format_interval(date)
            full_date_fmt = f"{check_interval} {hours}"
        else:
            full_date_fmt = hours
    return full_date, full_date_fmt, check_daily, check_interval


def format_date(date: datetime, check_daily: bool, check_interval: str, with_interval_formatted=False) -> str:
    """
    Format the train date for human readers. If we get a check_interval, then we will
    return the check_interval string itself plus the hours taken from date, otherwise we
    do a simple date formatting
    """
    if check_daily:
        if check_interval:
            if with_interval_formatted:
                return f"{format_interval(check_interval)} {date.hour}:{date.minute}"
            return f"{check_interval} {date.hour}:{date.minute}"
        return date.strftime("%H:%M")
    return date.strftime("%d/%m/%Y %H:%M")


def format_interval(interval: str) -> str:
    """
    Takes an interval string such as "lun,mar,mer" and formats it in the best possible way.
    format_interval("lun,mer,mar") -> "lun-mer"
    """
    interval = interval_split_pattern.split(interval)
    # Sort interval first
    ordered_days = [""] * 7
    for day in interval:
        ordered_days[days_mapping[day]] = day

    queue = list()
    t = itertools.groupby(ordered_days, key=lambda d: d != "")

    # If we get 3 days or more in a row we can compress them
    # before enqueueing them otherwise, simply append everything to the queue
    for is_full, group in t:
        if not is_full:
            continue
        days = list(group)
        if len(days) > 2:
            queue.append(f"{days[0]}-{days[-1]}")
        else:
            for el in days:
                queue.append(el)
    return ",".join(queue)
