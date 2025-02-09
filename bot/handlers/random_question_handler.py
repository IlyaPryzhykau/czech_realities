from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from bot.services.api_client import get_random_question
from bot.utils.question_formatter import format_question
from bot.constants_cz import (ERROR_NO_QUESTIONS_FOUND, BUTTON_SELECT_ANSWER)


async def handle_random_question(query, context: ContextTypes.DEFAULT_TYPE):
    """
    Fetches a random question from the API and sends it to the user.
    This mode is considered 'single' question mode.
    """
    question = await get_random_question()
    if not question:
        await query.message.reply_text(ERROR_NO_QUESTIONS_FOUND)
        return

    question_id = question.get('id')
    correct_answer = next((ans for ans in question.get('answers', [])
                           if ans.get('is_correct')), None)
    if correct_answer:
        context.user_data[f'correct_answer_{question_id}'] = correct_answer
    context.user_data['question_mode'] = 'single'  # Single-question mode

    messages, answer_messages, reply_markup = await format_question(question)

    # Send the main question
    for msg in messages:
        if msg['type'] == 'text':
            await query.message.reply_text(
                msg['content'],
                parse_mode='HTML',
                reply_markup=reply_markup
            )
        elif msg['type'] == 'photo':
            await query.message.reply_photo(
                photo=msg['content'],
                caption=msg.get('caption'),
                parse_mode='HTML',
                reply_markup=reply_markup
            )

    # If there are image answers, send them separately
    for ans in answer_messages:
        ans_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton(
                BUTTON_SELECT_ANSWER,
                callback_data=ans['callback_data']
            )]
        ])
        await query.message.reply_photo(
            photo=ans['content'],
            caption=ans['caption'],
            parse_mode='HTML',
            reply_markup=ans_markup
        )
