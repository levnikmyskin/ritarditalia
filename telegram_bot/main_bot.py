from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram.bot import Bot
from telegram_bot import stickers
from telegram.update import Update
from telegram import ParseMode
from telegram_bot.utils.token_parser import get_bot_token
from telegram_bot.utils.language_utils import set_language
from telegram_bot.utils import keyboard_utils, decorators, structs, trains_api, db_utils
from datetime import datetime
from telegram_bot.jobs.monitoring import get_status_message
from telegram_bot.jobs.monitoring import run as monitor
from config import BOT_DOMAIN
import app_strings
import logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)


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
        i, train_code, date, hours = update.message.text.split(" ")
        stations = trains_api.find_train_original_depart_station(train_code)
        if len(stations) > 1:
            # TODO ask user which of the stations he wants
            pass
        else:
            if date != "sempre":
                full_date = datetime.strptime(f"{date} {hours}", "%d/%m/%Y %H:%M")
            else:
                full_date = datetime.strptime(f"{hours}", "%H:%M")
            logging.debug(f"GOT: {train_code}, {date}, {hours}, {stations}")
            train = structs.Train(
                id=-1,
                code=train_code,
                depart_stat=stations[0],
                depart_date=full_date,
                user=update.message.from_user.id,
                checked=0,
                check_daily=date == "sempre"
            )
            db_utils.insert_train_in_db(train, conn)
            full_date_fmt = full_date.strftime("%d/%m/%Y %H:%M") if date != "sempre" else full_date.strftime("%H:%M")
            message = f"{_(app_strings.added_train)}Treno numero: {train.code};\n" \
                f"Parte da: {db_utils.get_station_from_code(train.depart_stat, conn).name};\n" \
                f"Tua partenza ore: {full_date_fmt}"
            bot.send_sticker(update.message.from_user.id, stickers.drake_approving)
            update.message.reply_text(message)
    except Exception as e:
        logging.error(e)
        bot.send_sticker(update.message.from_user.id, stickers.blackman_crying)
        update.message.reply_text(_(app_strings.error_adding_train))


@decorators.set_language
def train_status_list(bot: Bot, update: Update, conn):
    train_keyboard = keyboard_utils.train_list_keyboard("status", update.effective_user.id, conn)
    update.message.reply_text(_(app_strings.your_trains_status), reply_markup=train_keyboard)


@decorators.set_language
def train_delete_list(bot: Bot, update: Update, conn):
    train_keyboard = keyboard_utils.train_list_keyboard("delete", update.effective_user.id, conn)
    update.message.reply_text(_(app_strings.your_trains_deleting), reply_markup=train_keyboard)


def train_status(bot: Bot, update: Update):
    conn = db_utils.connect_db()
    cb_data = update.callback_query.data
    chat_id = update.effective_user.id
    train_id = update.callback_query.data.split("status")[1]

    train = db_utils.get_train(train_id, conn)
    status = trains_api.get_train_status(train.depart_stat, train.code)
    message, ok = get_status_message(status, train, conn, lang=db_utils.get_user(conn, chat_id=chat_id).lang)
    # We send a message instead of a notification,
    # but we still have to answer the callback query
    update.callback_query.answer()
    if not ok:
        logging.error(message)
        bot.send_sticker(update.callback_query.from_user.id, stickers.blackman_crying)
        bot.send_message(update.callback_query.from_user.id, message)
    else:
        bot.send_message(update.callback_query.from_user.id, message)
    conn.close()


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
    update.message.reply_text(helps.get(command[1], "Riprova"), parse_mode=ParseMode.MARKDOWN)


def main():
    token = get_bot_token()
    updater = Updater(token=token)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('monello', change_lang_monello))
    updater.dispatcher.add_handler(CommandHandler('monitora', add_train_to_monitor))
    updater.dispatcher.add_handler(CommandHandler('status', train_status_list))
    updater.dispatcher.add_handler(CommandHandler('delete', train_delete_list))
    updater.dispatcher.add_handler(CommandHandler('italian', change_lang_italian))
    updater.dispatcher.add_handler(CommandHandler('english', change_lang_english))
    updater.dispatcher.add_handler(CommandHandler('help', commands_help))
    updater.dispatcher.add_handler(CallbackQueryHandler(callback=train_status, pattern=r'status \d+'))
    updater.dispatcher.add_handler(CallbackQueryHandler(callback=delete_train, pattern=r'delete \d+'))
    updater.job_queue.run_repeating(monitor, interval=3600, first=0)
    updater.start_webhook(
        listen='0.0.0.0',
        port=5000,
        url_path=token,
        webhook_url=f'https://{BOT_DOMAIN}/{token}'
    )
    updater.idle()
    

if __name__ == '__main__':
    main()
