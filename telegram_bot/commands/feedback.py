import logging
import app_strings
from telegram import Update, Bot
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, filters
from telegram_bot.utils import decorators, db_utils


@decorators.set_language
def feedback_entry_point(bot: Bot, update: Update, conn):
    update.message.reply_text(_(app_strings.send_feedback))
    return 0


@decorators.set_language
def register_feedback(bot: Bot, update: Update, conn):
    try:
        feedback = update.effective_message.text
        db_utils.store_feedback(feedback, update.effective_chat.id, conn)
        update.message.reply_text(_(app_strings.thanks_feedback))
        return ConversationHandler.END
    except Exception as e:
        logging.error(e)
        return 0


@decorators.set_language
def stop_conversation(bot: Bot, update: Update, conn):
    update.message.reply_text(_(app_strings.stop_conversation))
    return ConversationHandler.END


entry_point = (CommandHandler("feedback", feedback_entry_point),)
states = {
    0: (MessageHandler(filters.Filters.text, callback=register_feedback),)
}
fallbacks = [
    CommandHandler("stop", stop_conversation),
    MessageHandler(
        filters.Filters.all,
        callback=lambda b, u: u.message.reply_text(_(app_strings.conversation_fallback))
    )
]