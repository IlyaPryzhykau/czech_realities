import logging
from telegram import Update
from telegram.ext import ContextTypes

from bot.handlers.random_ticket_handler import handle_random_ticket
from bot.handlers.topic_handler import handle_choose_topic
from bot.handlers.random_question_handler import handle_random_question
from bot.constants_cz import ERROR_UNKNOWN_MENU


async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Distributes user's choice in the main menu to the correct handler.
    """
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == 'choose_topic':
        await handle_choose_topic(query, context)

    elif data == 'random_question':
        await handle_random_question(query, context)

    elif data == 'random_ticket':
        await handle_random_ticket(update, context)

    else:
        await query.message.reply_text(ERROR_UNKNOWN_MENU)
