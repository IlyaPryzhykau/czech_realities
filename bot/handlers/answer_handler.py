import logging

from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from bot.constants_cz import (
    ERROR_NO_ANSWER, ANSWER_CORRECT, ANSWER_INCORRECT,
    BUTTON_CONTINUE, BUTTON_NEXT_QUESTION, BUTTON_MAIN_MENU
)

logger = logging.getLogger(__name__)


async def handle_answer_callback(update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the user's answer callback. Determines whether the selected answer
    is correct or not, updates the user's correct answer counter, and edits
    the message to display feedback.
    """
    query = update.callback_query
    await query.answer()

    _, question_id, answer_id = query.data.split('_')
    question_id = int(question_id)
    answer_id = int(answer_id)

    correct_answer = context.user_data.get(f'correct_answer_{question_id}')
    mode = context.user_data.get('question_mode', 'single')

    # If correct_answer not found in context
    if not correct_answer:
        await query.message.reply_text(ERROR_NO_ANSWER)
        return

    is_correct = (answer_id == correct_answer['id'])

    if is_correct:
        context.user_data['correct_answers'] = context.user_data.get(
            'correct_answers', 0) + 1
        result_text = ANSWER_CORRECT.format(answer=correct_answer['text'])
    else:
        result_text = ANSWER_INCORRECT.format(answer=correct_answer['text'])

    new_text = ((query.message.text or query.message.caption or '')
                + f'\n\n{result_text}')

    # Depending on the mode, create different reply_markup
    options = []
    if mode in ['topic', 'ticket']:
        options.append(
            [InlineKeyboardButton(
                BUTTON_CONTINUE,
                callback_data='next_question'
            )]
        )
    else:
        options.append(
            [InlineKeyboardButton(
                BUTTON_NEXT_QUESTION,
                callback_data='random_question'
            )]
        )
        options.append(
            [InlineKeyboardButton(
                BUTTON_MAIN_MENU,
                callback_data='main_menu'
            )]
        )

    reply_markup = InlineKeyboardMarkup(options)

    # Edit the caption if it's a photo, otherwise edit the text
    if query.message.photo:
        await query.message.edit_caption(
            new_text,
            parse_mode='HTML',
            reply_markup=reply_markup
        )
    else:
        await query.message.edit_text(
            new_text,
            parse_mode='HTML',
            reply_markup=reply_markup
        )
