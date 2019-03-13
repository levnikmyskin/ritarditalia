from telegram_bot.utils import db_utils
from telegram_bot.utils.language_utils import set_language as language


def set_language(func):
    def wrapper(bot, update):
        conn = db_utils.connect_db()
        user = db_utils.get_user(conn, chat_id=str(update.effective_user.id))
        language(user.lang)
        func(bot, update, conn)
        conn.close()
    return wrapper
