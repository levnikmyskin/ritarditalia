import logging

from telegram import Update, Bot
from telegram.ext import RegexHandler, CommandHandler, ConversationHandler, MessageHandler, Filters, \
    CallbackQueryHandler

from telegram_bot import stickers
from telegram_bot.jobs.monitoring import interval_regex, interval_days, days_mapping
from telegram_bot.utils import trains_api, db_utils, structs, keyboard_utils
from telegram_bot.utils import decorators
from telegram_bot.utils.date_helper import parse_date_from_user_message, format_date, format_interval
from telegram_bot.utils.exceptions import TrainInPastError, WrongDateFormatError
from telegram_bot.utils.notifications import get_train_info_message
from telegram_bot.utils.structs import MonitorConversationStates
import app_strings


class MonitorConversationHandler(ConversationHandler):

    def __init__(self, timeout_callback, *args, **kwargs):
        self.timeout_callback = timeout_callback
        super().__init__(*args, **kwargs)

    def _trigger_timeout(self, bot, job):
        super()._trigger_timeout(bot, job)
        self.timeout_callback(bot, job, self.current_conversation[0])


class TrainDict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


@decorators.set_language
def monitor_by_step_entrypoint(bot: Bot, update: Update, conn):
    update.message.reply_text(_(app_strings.monitor_step_entrypoint))
    return MonitorConversationStates.SEND_TRAIN_CODE


@decorators.set_language
def register_train_code(bot: Bot, update: Update, conn):
    try:
        train_code = update.effective_message.text
        stations = trains_api.find_train_original_depart_station(train_code)
        if len(stations) == 0:
            bot.send_sticker(update.effective_chat.id, stickers.sad_cat)
            update.message.reply_text(f"{_(app_strings.api_error)}\n{_(app_strings.use_stop_to_end)}")
            return MonitorConversationStates.SEND_TRAIN_CODE
        elif len(stations) > 1:
            data[update.effective_chat.id] = TrainDict({"code": train_code})
            update.message.reply_text(
                _(app_strings.multiple_stations_found),
                reply_markup=keyboard_utils.stations_keyboard(stations)
            )
            return MonitorConversationStates.SEND_STATION

        return __prepare_for_sending_date(update, stations[0][1], train_code, conn)
    except Exception as e:
        logging.error(e)
        bot.send_sticker(update.effective_chat.id, sticker=stickers.blackman_crying)
        update.message.reply_text(f"{_(app_strings.error_adding_train)}\n{_(app_strings.monitor_step_entrypoint)}")
        return MonitorConversationStates.SEND_TRAIN_CODE


@decorators.set_language
def register_station(bot: Bot, update: Update, conn):
    try:
        train_data = data[update.effective_chat.id]
        station_code = update.effective_message.text.split(')')[0]
        return __prepare_for_sending_date(update, station_code, train_data.code, conn)
    except Exception as e:
        logging.error(e)
        bot.send_sticker(update.message.from_user.id, stickers.blackman_crying)
        update.message.reply_text(f"{_(app_strings.generic_error)}\n{_(app_strings.monitor_step_entrypoint)}",
                                  reply_markup=keyboard_utils.ReplyKeyboardRemove())
        return MonitorConversationStates.SEND_TRAIN_CODE


def __prepare_for_sending_date(update, station_code, train_code, conn):
    station_code = db_utils.get_station_from_code(station_code, conn)
    days_keyboard = keyboard_utils.interval_keyboard(interval_days)
    update.message.reply_text(f"Treno: {train_code}\n"
                              f"Parte da: {station_code.name}"
                              f"\n\n{_(app_strings.monitor_step_date)}", reply_markup=days_keyboard)
    data[update.effective_chat.id] = TrainDict({"code": train_code, "depart_stat": station_code.code,
                                                "human_stat": station_code.name})
    return MonitorConversationStates.SEND_DATE


@decorators.set_language
def register_date(bot: Bot, update: Update, conn):
    train_data = data[update.effective_chat.id]
    train_data.date = update.effective_message.text
    update.message.reply_text(_(app_strings.monitor_step_hours))
    return MonitorConversationStates.SEND_HOURS


@decorators.set_language
def register_interval(bot: Bot, update: Update, conn):
    train_data = data[update.effective_chat.id]
    interval_set = train_data.setdefault("interval", set())
    cb_day = update.callback_query.data
    cb_day = cb_day[:3]  # remove tick in case it's there
    if cb_day in interval_set:
        interval_set.remove(cb_day)
    else:
        interval_set.add(cb_day)
    days_keyboard = keyboard_utils.interval_keyboard(
        map(lambda d: f"{d}{stickers.tick}" if d in interval_set else d, interval_days)
    )
    update.callback_query.message.edit_reply_markup(reply_markup=days_keyboard)
    update.callback_query.answer()
    return MonitorConversationStates.SEND_DATE


@decorators.set_language
def confirm_interval(bot: Bot, update: Update, conn):
    train_data = data[update.effective_chat.id]
    train_data.date = ",".join(train_data.interval)
    update.message.reply_text(_(app_strings.monitor_step_hours))
    return MonitorConversationStates.SEND_HOURS


@decorators.set_language
def register_hours(bot: Bot, update: Update, conn):
    try:
        train_data = data[update.effective_chat.id]
        full_date, full_date_fmt, check_daily, check_interval = parse_date_from_user_message(
            train_data.date, update.effective_message.text
        )
        train_data.depart_date = full_date
        train_data.check_daily = check_daily
        train_data.check_interval = check_interval
        update.message.reply_text(f"Treno: {train_data.code}\n"
                                  f"Parte da: {train_data.human_stat}\n"
                                  f"Tua partenza: {full_date_fmt}"
                                  f"\n\nSe vuoi, puoi aggiungere carrozza e posto (es. 4 11D), altrimenti "
                                  f"usa /ok per confermare, /stop per cancellare")
        return MonitorConversationStates.SEND_COACH_SEAT
    except WrongDateFormatError as e:
        logging.error(e)
        bot.send_sticker(update.effective_chat.id, stickers.toninelli)
        update.message.reply_text(_(app_strings.wrong_date))
    except Exception as e:
        logging.error(e)
        bot.send_sticker(update.effective_chat.id, stickers.tom_not_understanding)
        update.message.reply_text(_(app_strings.generic_error))
        return MonitorConversationStates.SEND_HOURS


@decorators.set_language
def register_coach_seat(bot: Bot, update: Update, conn):
    train_data = data[update.effective_chat.id]
    coach, seat = update.effective_message.text.split(" ")
    train_data.coach = coach
    train_data.seat = seat
    update.message.reply_text(f"Carrozza {coach}, Posto {seat}\nUsa /ok per confermare, /stop per cancellare")
    return MonitorConversationStates.CONFIRM_MONITORING


@decorators.set_language
def confirm_monitoring(bot: Bot, update: Update, conn):
    try:
        train_data = data[update.effective_chat.id]
        train = structs.Train(
            id=-1,
            code=train_data.code,
            depart_stat=train_data.depart_stat,
            depart_date=train_data.depart_date,
            user=update.effective_chat.id,
            checked=0,
            check_daily=train_data.check_daily,
            check_interval=train_data.check_interval,
            coach=train_data.coach,
            seat=train_data.seat.upper() if train_data.seat else None
        )
        db_utils.insert_train_in_db(train, conn)
        bot.send_sticker(update.effective_chat.id, stickers.drake_approving)
        date_fmt = format_date(train.depart_date, train.check_daily, train.check_interval)
        update.message.reply_text(f"{_(app_strings.added_train)}{get_train_info_message(train_data, date_fmt, conn)}")
    except TrainInPastError as e:
        logging.error(e)
        bot.send_sticker(update.message.from_user.id, stickers.tom_puzzled)
        update.message.reply_text(_(app_strings.train_in_past_error))
    except Exception as e:
        logging.error(e)
        bot.send_sticker(update.message.from_user.id, stickers.blackman_crying)
        update.message.reply_text(_(app_strings.error_adding_train))
    finally:
        del data[update.effective_chat.id]
    return ConversationHandler.END


@decorators.set_language
def stop_monitoring_conversation(bot: Bot, update: Update, conn):
    try:
        del data[update.effective_chat.id]
        update.message.reply_text(_(app_strings.stop_conversation))
    except Exception as e:
        logging.error(e)
    finally:
        return ConversationHandler.END


def on_conversation_timeout(bot: Bot, job, user):
    try:
        del data[user]
        update.message.reply_text(_(app_strings.stop_conversation))
    except Exception as e:
        logging.error(e)
    finally:
        return ConversationHandler.END


data = dict()
entry_points = (RegexHandler(r'^\/monitora$', monitor_by_step_entrypoint),)
states = {
    MonitorConversationStates.SEND_TRAIN_CODE: (RegexHandler(r'^\d+$', register_train_code),),
    MonitorConversationStates.SEND_STATION: (RegexHandler(r'^.+\).+', register_station),),
    MonitorConversationStates.SEND_DATE: (RegexHandler(r'^\d{2}/\d{2}/\d{4}$', register_date),
                                          # Todo we could improve this pattern
                                          CallbackQueryHandler(callback=register_interval, pattern=r'\w{3}.?'),
                                          CommandHandler("ok", confirm_interval)
                                          ),
    MonitorConversationStates.SEND_HOURS: (RegexHandler(r'^\d{1,2}:\d{2}', register_hours),),
    MonitorConversationStates.SEND_COACH_SEAT: (RegexHandler(r'^\d+\s\d+\w$', register_coach_seat),
                                                CommandHandler("ok", confirm_monitoring)),
    MonitorConversationStates.CONFIRM_MONITORING: (CommandHandler("ok", confirm_monitoring),)
}
fallbacks = [
    CommandHandler("stop", stop_monitoring_conversation),
    MessageHandler(
        Filters.all,
        callback=lambda b, u: u.message.reply_text(_(app_strings.conversation_fallback))
    )
]
