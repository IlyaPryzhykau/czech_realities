import asyncio
import platform
import logging

from telegram.ext import (ApplicationBuilder, CommandHandler, MessageHandler,
                          CallbackQueryHandler, filters)

from bot.config import BOT_TOKEN
from bot.handlers.start_handler import start_command
from bot.handlers.help_handler import help_command
from bot.handlers.menu_handler import menu_callback
from bot.handlers.main_menu_handler import handle_main_menu
from bot.handlers.next_question_handler import send_next_question
from bot.handlers.topic_handler import (handle_choose_topic,
                                        handle_topic_selection)
from bot.handlers.answer_handler import handle_answer_callback
from bot.handlers.random_ticket_handler import handle_random_ticket


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def build_bot():
    """
    Builds the application (bot) with all the necessary handlers.
    """
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))

    # Text-based "reply buttons"
    app.add_handler(
        MessageHandler(
            filters.TEXT & filters.Regex(r'🚀 Start'),
            start_command
        )
    )
    app.add_handler(
        MessageHandler(
            filters.TEXT & filters.Regex(r'ℹ️ Help'),
            help_command
        )
    )

    # Inline callback query handlers
    # Menu
    app.add_handler(
        CallbackQueryHandler(
            menu_callback,
            pattern=r'^(choose_topic|random_question|random_ticket)$'
        )
    )
    app.add_handler(
        CallbackQueryHandler(
            handle_main_menu,
            pattern=r'^main_menu$'
        )
    )
    app.add_handler(
        CallbackQueryHandler(
            send_next_question,
            pattern=r'^next_question'
        )
    )

    # Topics
    app.add_handler(
        CallbackQueryHandler(
            handle_choose_topic,
            pattern=r'^choose_topic$'
        )
    )
    app.add_handler(
        CallbackQueryHandler(
            handle_topic_selection,
            pattern=r'^topic_\d+$'
        )
    )

    # Answers
    app.add_handler(
        CallbackQueryHandler(
            handle_answer_callback,
            pattern=r'^answer_\d+_\d+$'
        )
    )

    # Random ticket
    app.add_handler(
        CallbackQueryHandler(
            handle_random_ticket,
            pattern='^random_ticket$'
        )
    )

    return app


def main():
    """
    Entry point: sets up the event loop policy on Windows if needed,
    builds the bot, and runs it in polling mode.
    """
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    app = build_bot()
    logger.info('Bot started in polling mode')

    app.run_polling(
        drop_pending_updates=True,
        allowed_updates=['message', 'callback_query'],
        close_loop=False
    )


if __name__ == '__main__':
    main()
