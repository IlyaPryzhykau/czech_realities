import logging
from telegram import (Update, ReplyKeyboardMarkup, InlineKeyboardButton,
                      InlineKeyboardMarkup)
from telegram.ext import ContextTypes
from bot.constants_cz import (WELCOME_TITLE, BOT_FEATURES, TEST_STRUCTURE,
                              QUESTION_FORMAT, IMPORTANT_INFO,BUTTON_START,
                              BUTTON_HELP, BUTTON_CHOOSE_TOPIC,
                              BUTTON_RANDOM_QUESTION,BUTTON_RANDOM_TICKET,
                              START_CHOOSE_OPTION)

logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the /start command and '🚀 Start' button.
    Sends info about the bot and the main test menu.
    """
    main_keyboard = [
        [BUTTON_START, BUTTON_HELP]
    ]
    reply_markup = ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)

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

    # Delete previous message
    if update.message:
        await update.message.delete()

    await update.message.reply_text(
        f'{WELCOME_TITLE}\n{BOT_FEATURES}\n{TEST_STRUCTURE}\n'
        f'{QUESTION_FORMAT}\n{IMPORTANT_INFO}',
        parse_mode='HTML',
        reply_markup=reply_markup
    )

    await update.message.reply_text(
        START_CHOOSE_OPTION,
        reply_markup=inline_markup
    )
