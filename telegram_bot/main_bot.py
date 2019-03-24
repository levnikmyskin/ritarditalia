from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, ConversationHandler
from telegram.bot import Bot
from telegram_bot import stickers
from telegram.update import Update
from telegram import ParseMode

from telegram_bot.commands import monitor_by_step, feedback
from telegram_bot.commands.monitor_by_step import MonitorConversationHandler, on_conversation_timeout
from telegram_bot.utils.date_helper import parse_date_from_user_message, format_date
from telegram_bot.utils.notifications import get_train_info_message
from telegram_bot.utils.structs import TrainStatus
from telegram_bot.utils.token_parser import get_bot_token
from telegram_bot.utils.language_utils import set_language
from telegram_bot.utils import keyboard_utils, decorators, structs, trains_api, db_utils, pdf_extraction
from telegram_bot.utils.exceptions import TrainInPastError
from datetime import timedelta
from telegram_bot.jobs.monitoring import get_status_message, run as monitor
from config import BOT_DOMAIN
import fitz
import app_strings
import logging

logging.basicConfig(filename='app.log', level=logging.DEBUG, format="%(asctime)-15s %(message)s")


def start(bot: Bot, update: Update):
    logging.info("Received start command")
    conn = db_utils.connect_db()
    user = db_utils.get_or_save_user(
        str(update.message.from_user.id),
        update.message.from_user.first_name,
        email="",
        notification_via="telegram",
        conn=conn
    )
    set_language(user.lang)
    update.message.reply_text(_(app_strings.start_message), parse_mode=ParseMode.MARKDOWN)
    bot.send_message(update.message.from_user.id, text=_(app_strings.command_message))
    conn.close()


def change_lang_monello(bot: Bot, update: Update):
    conn = db_utils.connect_db()
    db_utils.update_user_lang(conn, chat_id=str(update.message.from_user.id), lang='mn')
    set_language('mn')
    update.message.reply_text(_(app_strings.language_switched))
    conn.close()


def change_lang_italian(bot: Bot, update: Update):
    conn = db_utils.connect_db()
    db_utils.update_user_lang(conn, chat_id=str(update.message.from_user.id))
    set_language('it')
    update.message.reply_text(_(app_strings.language_switched))
    conn.close()


def change_lang_english(bot: Bot, update: Update):
    update.message.reply_text("The english language is not available yet :(")


@decorators.set_language
def add_train_to_monitor(bot: Bot, update: Update, conn):
    try:
        split = update.message.text.split(" ")
        train_code, date, hours = split[1:4]
        coach, seat = split[4:6] if len(split) == 6 else (None, None)
        stations = trains_api.find_train_original_depart_station(train_code)
        if len(stations) == 0:
            bot.send_sticker(update.effective_chat.id, stickers.sad_cat)
            update.message.reply_text(_(app_strings.api_error))
            return
        if len(stations) > 1:
            # TODO ask user which of the stations he wants
            pass
        else:
            full_date, full_date_fmt, check_daily, check_interval = parse_date_from_user_message(date, hours)

            logging.debug(f"GOT: {train_code}, {date}, {hours}, {stations}")
            train = structs.Train(
                id=-1,
                code=train_code,
                depart_stat=stations[0][1],
                depart_date=full_date,
                user=update.effective_chat.id,
                checked=0,
                check_daily=check_daily,
                check_interval=check_interval,
                coach=coach,
                seat=seat.upper() if seat is not None else None
            )
            db_utils.insert_train_in_db(train, conn)
            message = f"{_(app_strings.added_train)}{get_train_info_message(train, full_date_fmt, conn)}"
            bot.send_sticker(update.message.from_user.id, stickers.drake_approving)
            update.message.reply_text(message)
    except TrainInPastError as e:
        logging.error(e)
        bot.send_sticker(update.message.from_user.id, stickers.tom_puzzled)
        update.message.reply_text(_(app_strings.train_in_past_error))
    except Exception as e:
        logging.error(e)
        bot.send_sticker(update.message.from_user.id, stickers.blackman_crying)
        update.message.reply_text(_(app_strings.error_adding_train))


@decorators.set_language
def train_status_list(bot: Bot, update: Update, conn):
    train_keyboard = keyboard_utils.train_list_keyboard("status", update.effective_chat.id, conn)
    update.message.reply_text(_(app_strings.your_trains_status), reply_markup=train_keyboard)


@decorators.set_language
def train_delete_list(bot: Bot, update: Update, conn):
    train_keyboard = keyboard_utils.train_list_keyboard("delete", update.effective_chat.id, conn)
    update.message.reply_text(_(app_strings.your_trains_deleting), reply_markup=train_keyboard)


@decorators.set_language
def train_info_list(bot: Bot, update: Update, conn):
    train_keyboard = keyboard_utils.train_list_keyboard("info", update.effective_chat.id, conn)
    update.message.reply_text(_(app_strings.your_trains_info), reply_markup=train_keyboard)


@decorators.set_language
def train_status(bot: Bot, update: Update, conn):
    cb_data = update.callback_query.data
    chat_id = update.effective_user.id
    train_id = update.callback_query.data.split("status")[1]

    train = db_utils.get_train(train_id, conn)
    status = trains_api.get_train_status(train.depart_stat, train.code)
    message, status = get_status_message(status, train, conn, lang=db_utils.get_user(conn, chat_id=chat_id).lang)
    # We send a message instead of a notification,
    # but we still have to answer the callback query
    update.callback_query.answer()
    if status == TrainStatus.AVAILABLE:
        bot.send_message(update.callback_query.from_user.id, message)
    else:
        bot.send_sticker(update.callback_query.from_user.id, stickers.blackman_crying)
        bot.send_message(update.callback_query.from_user.id, message)


@decorators.set_language
def delete_train(bot: Bot, update: Update, conn):
    train_id = update.callback_query.data.split('delete')[1]
    chat_id = update.callback_query.from_user.id
    try:
        db_utils.delete_train(train_id, conn)
        updated_keyboard = keyboard_utils.train_list_keyboard("delete", chat_id, conn)
        update.callback_query.message.edit_reply_markup(reply_markup=updated_keyboard)
        bot.send_sticker(chat_id, stickers.destruction_100)
        bot.send_message(chat_id, _(app_strings.train_deleted))
    except Exception as e:
        logging.error(e)
        bot.send_sticker(chat_id, stickers.blackman_crying)
        bot.send_message(chat_id, _(app_strings.error_deleting_train))
    finally:
        update.callback_query.answer()


@decorators.set_language
def train_info(bot: Bot, update: Update, conn):
    train_id = update.callback_query.data.split('info')[1]
    try:
        train = db_utils.get_train(train_id, conn)
        date_fmt = format_date(train.depart_date, train.check_daily, train.check_interval)
        message = get_train_info_message(train, date_fmt, conn)
        bot.send_message(update.effective_chat.id, message)
    except Exception as e:
        logging.error(e)
        bot.send_sticker(update.effective_chat.id, stickers.toninelli)
        bot.send_message(update.effective_chat.id, _(app_strings.generic_error))
    finally:
        update.callback_query.answer()


@decorators.set_language
def commands_help(bot: Bot, update: Update, conn):
    helps = {
        "monello": _(app_strings.monello_help),
        "monitora": _(app_strings.monitor_help),
        "status": _(app_strings.status_help),
        "delete": _(app_strings.delete_help),
        "italian": _(app_strings.italian_help),
        "english": _(app_strings.english_help)
    }
    command = update.effective_message.text.split(" ")
    if len(command) == 1:
        update.message.reply_text(_(app_strings.help_error), parse_mode=ParseMode.MARKDOWN)
    update.message.reply_text(helps.get(command[1], "Riprova"), parse_mode=ParseMode.MARKDOWN)


@decorators.set_language
def train_from_pdf(bot: Bot, update: Update, conn):
    try:
        buffer = update.message.document.get_file().download_as_bytearray()
        document = fitz.Document(stream=buffer, filetype="pdf")
        trains = pdf_extraction.extract_info_from_pdf(document, update.effective_chat.id)
        if not trains:
            raise Exception(f"Train extraction list was empty :( {trains}")
        message = f"{_(app_strings.added_train)}"
        for train in trains:
            db_utils.insert_train_in_db(train, conn, False)
            message += get_train_info_message(train, format_date(train.depart_date, ""), conn)
        conn.commit()
        bot.send_sticker(update.message.from_user.id, stickers.drake_approving)
        update.message.reply_text(message)
    except TrainInPastError as e:
        logging.error(e)
        bot.send_sticker(update.message.from_user.id, stickers.tom_puzzled)
        update.message.reply_text(_(app_strings.train_in_past_error))
    except Exception as e:
        logging.error(e)
        bot.send_sticker(update.effective_chat.id, stickers.blackman_crying)
        bot.send_message(update.effective_chat.id, _(app_strings.error_pdf))


def main():
    token = get_bot_token()
    updater = Updater(token=token)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('monello', change_lang_monello))
    updater.dispatcher.add_handler(MonitorConversationHandler(
        timeout_callback=on_conversation_timeout,
        entry_points=monitor_by_step.entry_points,
        states=monitor_by_step.states,
        fallbacks=monitor_by_step.fallbacks,
        conversation_timeout=timedelta(minutes=30)
    )
    )
    updater.dispatcher.add_handler(CommandHandler('monitora', add_train_to_monitor))
    updater.dispatcher.add_handler(CommandHandler('status', train_status_list))
    updater.dispatcher.add_handler(CommandHandler('delete', train_delete_list))
    updater.dispatcher.add_handler(CommandHandler('italian', change_lang_italian))
    updater.dispatcher.add_handler(CommandHandler('english', change_lang_english))
    updater.dispatcher.add_handler(CommandHandler('help', commands_help))
    updater.dispatcher.add_handler(CallbackQueryHandler(callback=train_status, pattern=r'status \d+'))
    updater.dispatcher.add_handler(CallbackQueryHandler(callback=delete_train, pattern=r'delete \d+'))
    updater.dispatcher.add_handler(MessageHandler(filters=Filters.document, callback=train_from_pdf))
    updater.dispatcher.add_handler(ConversationHandler(
        entry_points=feedback.entry_point,
        states=feedback.states,
        fallbacks=feedback.fallbacks,
        conversation_timeout=timedelta(minutes=30)
    ))
    updater.dispatcher.add_handler(CommandHandler("info", train_info_list))
    updater.dispatcher.add_handler(CallbackQueryHandler(callback=train_info, pattern=r'info \d+'))
    updater.job_queue.run_repeating(monitor, interval=2400, first=0)
    updater.start_polling()
    # updater.start_webhook(
    #     listen='0.0.0.0',
    #     port=5000,
    #     url_path=token,
    #     webhook_url=f'https://{BOT_DOMAIN}/{token}'
    # )
    updater.idle()


if __name__ == '__main__':
    main()
