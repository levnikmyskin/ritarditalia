import itertools
from telegram_bot.utils import db_utils
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
import app_strings


def grouper(iterable, n, fillvalue=None):
    # Collect data into fixed-length chunks or blocks
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)


def train_list_iterator(chat_id: str, conn) -> iter:
    all_trains = db_utils.get_all_trains(chat_id, conn)
    return grouper(all_trains, 2)


def train_list_keyboard(callback_key: str, chat_id: str, conn) -> InlineKeyboardMarkup:
    """
    Returns a keyboard containing at most two trains per row
    """
    trains = train_list_iterator(chat_id, conn)
    buttons = [
        [InlineKeyboardButton(f"{_(app_strings.train)} {el.code} {__get_train_date_for_keyboard(el)}",
                              callback_data=f"{callback_key} {el.id}") for el in group if el is not None]
        for group in trains
    ]
    return InlineKeyboardMarkup(buttons)


def interval_keyboard(days) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(day, callback_data=day) for day in group if day is not None]
        for group in grouper(days, 3)
    ]
    return InlineKeyboardMarkup(buttons)


def stations_keyboard(stations: (str, str)) -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(f"{station[1]}) {station[0]}") for station in group if station is not None]
        for group in grouper(stations, 3)
    ]
    return ReplyKeyboardMarkup(buttons, one_time_keyboard=True)


def __get_train_date_for_keyboard(train) -> str:
    if train.check_daily:
        return train.depart_date.strftime('%H:%M')
    return train.depart_date.strftime('%d/%m/%Y %H:%M')

