import logging

from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from bot.constants_cz import (
    HELP_INSTRUCTIONS, HELP_CHOOSE_OPTION,
    BUTTON_START, BUTTON_HELP, BUTTON_CHOOSE_TOPIC,
    BUTTON_RANDOM_QUESTION, BUTTON_RANDOM_TICKET
)

logger = logging.getLogger(__name__)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the /help command and the 'ℹ️ Help' reply button.
    Sends instructions on how to use the bot and an inline keyboard with test options.
    """
    # Reply keyboard (bottom)
    main_keyboard = [
        [BUTTON_START, BUTTON_HELP]
    ]
    reply_markup = ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)

    # Inline keyboard for test selection
    inline_keyboard = [
        [
            InlineKeyboardButton(
                BUTTON_CHOOSE_TOPIC,
                callback_data='choose_topic'
            ),
            InlineKeyboardButton(
                BUTTON_RANDOM_QUESTION,
                callback_data='random_question'
            ),
        ],
        [
            InlineKeyboardButton(
                BUTTON_RANDOM_TICKET,
                callback_data='random_ticket'
            )
        ]
    ]
    inline_markup = InlineKeyboardMarkup(inline_keyboard)

    # Delete previous message (to avoid spam)
    if update.message:
        await update.message.delete()

    # Send help instructions
    await update.message.reply_text(
        HELP_INSTRUCTIONS,
        reply_markup=reply_markup
    )
    await update.message.reply_text(
        HELP_CHOOSE_OPTION,
        reply_markup=inline_markup
    )
