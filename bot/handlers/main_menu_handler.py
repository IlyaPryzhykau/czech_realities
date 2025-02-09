from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from bot.constants_cz import (BUTTON_CHOOSE_TOPIC, BUTTON_RANDOM_QUESTION,
                              BUTTON_RANDOM_TICKET,MAIN_MENU_TITLE)


async def handle_main_menu(update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the 'main_menu' callback data. Presents a main menu for the user.
    """
    query = update.callback_query
    await query.answer()

    keyboard = [
        [
            InlineKeyboardButton(
                BUTTON_CHOOSE_TOPIC,
                callback_data='choose_topic'
            ),
            InlineKeyboardButton(
                BUTTON_RANDOM_QUESTION,
                callback_data='random_question'
            )
        ],
        [
            InlineKeyboardButton(
                BUTTON_RANDOM_TICKET,
                callback_data='random_ticket'
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_text(
        MAIN_MENU_TITLE,
        parse_mode='HTML',
        reply_markup=reply_markup
    )
