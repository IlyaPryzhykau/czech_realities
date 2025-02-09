import logging
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from bot.handlers.results_handler import show_results
from bot.utils.question_formatter import format_question
from bot.constants_cz import BUTTON_SELECT_ANSWER

logger = logging.getLogger(__name__)


async def send_next_question(
        update,
        context: ContextTypes.DEFAULT_TYPE,
        mode=None
):
    """
    Sends the next question to the user in 'topic' or 'ticket' mode.
    If questions are exhausted, calls show_results().
    """
    query = update.callback_query
    if query:
        await query.answer()

    # If mode is explicitly passed, store it in user_data
    if mode is not None:
        context.user_data['question_mode'] = mode
    else:
        mode = context.user_data.get('question_mode', 'topic')

    logger.info('DEBUG: Determined mode — %s', mode)

    # Use different user_data keys depending on mode
    questions_key = 'ticket_questions' if mode == 'ticket' \
        else 'topic_questions'
    questions = context.user_data.get(questions_key, [])

    index = context.user_data.get('current_question_index', 0)

    logger.debug('DEBUG: Current index %s, total questions: %s, mode: %s',
                 index, len(questions), mode)

    # If no more questions left, show final results
    if index >= len(questions):
        await show_results(query, context)
        return

    # Mark the current index in user_data
    context.user_data['current_question_index'] = index

    question = questions[index]
    logger.debug('DEBUG: Sending question: %s', question)

    # Store correct answer in user_data
    correct_answer = next((ans for ans in question.get('answers', [])
                           if ans.get('is_correct')), None)
    if correct_answer:
        context.user_data[f'correct_answer_{question["id"]}'] = correct_answer

    context.user_data['question_mode'] = mode

    messages, answer_messages, reply_markup = await format_question(question)

    # Send the main question part(s)
    sent_msg = None
    for msg in messages:
        if msg['type'] == 'text':
            sent_msg = await query.message.reply_text(
                msg['content'],
                parse_mode='HTML',
                reply_markup=reply_markup
            )
        elif msg['type'] == 'photo':
            sent_msg = await query.message.reply_photo(
                photo=msg['content'],
                caption=msg.get('caption'),
                parse_mode='HTML',
                reply_markup=reply_markup
            )

    # Increase index after sending the question
    context.user_data['current_question_index'] += 1

    # Store the ID of the last question message if needed
    if sent_msg:
        context.user_data['last_question_message'] = sent_msg.message_id

    # If there are answer images, send them separately
    sent_answers = []
    for ans in answer_messages:
        # Each answer image has its own button
        button_markup = InlineKeyboardMarkup([[
            InlineKeyboardButton(
                BUTTON_SELECT_ANSWER,
                callback_data=ans['callback_data']
            )
        ]])
        msg = await query.message.reply_photo(
            photo=ans['content'],
            caption=ans['caption'],
            parse_mode='HTML',
            reply_markup=button_markup
        )
        sent_answers.append(msg.message_id)

    context.user_data['last_answer_messages'] = sent_answers
