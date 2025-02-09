import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from bot.services.api_client import get_topics, get_questions_by_topic
from bot.handlers.next_question_handler import send_next_question
from bot.constants_cz import CHOOSE_TOPIC_TEXT, ERROR_NO_QUESTIONS_TOPIC

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


async def handle_choose_topic(query, context: ContextTypes.DEFAULT_TYPE):
    """
    Fetches a list of topics and displays them to the user as inline buttons.
    """
    topics = await get_topics()

    keyboard = []
    for topic in topics:
        topic_id = str(topic['id']).strip()
        topic_name = str(topic['name']).strip()

        button = InlineKeyboardButton(
            text=topic_name,
            callback_data=f'topic_{topic_id}'
        )
        keyboard.append([button])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        CHOOSE_TOPIC_TEXT,
        reply_markup=reply_markup
    )


async def handle_topic_selection(update, context: ContextTypes.DEFAULT_TYPE):
    """
    Loads questions by the chosen topic and starts the 'topic' mode test.
    """
    query = update.callback_query
    await query.answer()

    _, topic_id = query.data.split('_')
    topic_id = int(topic_id)

    questions = await get_questions_by_topic(topic_id)
    logger.debug('DEBUG: Questions for topic %s: %s', topic_id, questions)

    if not questions:
        await query.message.reply_text(ERROR_NO_QUESTIONS_TOPIC)
        return

    context.user_data['question_mode'] = 'topic'
    context.user_data['topic_questions'] = questions
    context.user_data['current_question_index'] = 0
    context.user_data['correct_answers'] = 0
    context.user_data['total_questions'] = len(questions)

    logger.info('DEBUG: Stored topic questions in user_data.')

    await send_next_question(update, context)
