import logging
from telegram import Update
from telegram.ext import ContextTypes

from bot.services.api_client import get_random_ticket
from bot.handlers.next_question_handler import send_next_question
from bot.constants_cz import ERROR_TICKET_LOAD

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


async def handle_random_ticket(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):
    """
    Fetches a random ticket (set of questions) from the API
    and starts the 'ticket' mode test.
    """
    query = update.callback_query
    await query.answer()

    questions = await get_random_ticket()
    logger.debug('DEBUG: Received random ticket: %s', questions)

    if not questions:
        await query.message.reply_text(ERROR_TICKET_LOAD)
        return

    context.user_data['question_mode'] = 'ticket'
    context.user_data['ticket_questions'] = questions
    context.user_data['current_question_index'] = 0
    context.user_data['correct_answers'] = 0
    context.user_data['total_questions'] = len(questions)

    logger.info('DEBUG: Saved ticket questions to user_data.')

    await send_next_question(update, context, mode='ticket')
