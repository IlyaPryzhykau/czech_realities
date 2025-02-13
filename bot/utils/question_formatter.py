"""
Utility functions that help format questions
and answers for sending via Telegram.
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


async def format_question(
        question: dict,
        question_number: int | None = None,
        total_questions: int | None = None
) -> tuple:
    """
    Formats a question from the database and returns a tuple:
    (messages, image_answers, reply_markup)

    :param question: dict
        Dictionary containing the question data.
    :param question_number: int | None
        The current question number in the sequence (1-based index).
    :param total_questions: int | None
        The total number of questions in the set.
    :return: tuple
        (messages, image_answers, reply_markup)
        - messages: List of message dictionaries (type='text' or
            'photo', content=..., caption=...).
        - image_answers: List of image-based answers (if any).
        - reply_markup: InlineKeyboardMarkup for text-based answers (if any).
    """
    messages = []
    image_answers = []

    question_id = question.get('id')
    question_text = question.get('text', '❓ Otázka chybí')
    topic_name = question.get('topic', {}).get('name', 'Neznámé téma')
    image_url = question.get('image_url')

    answers = question.get('answers', [])
    has_image_answers = any(ans.get('image_url') for ans in answers)

    if question_number and total_questions:
        header_text = f'<b>Otázka {question_number}/{total_questions}</b>\n\n'
    else:
        header_text = f'<b>Otázka </b>\n\n'

    message_text = (
        f'🎯 {header_text}'
        f'📌 <b>Téma:</b> {topic_name}\n\n'
        f'❓ <b>Otázka:</b>\n{question_text}\n\n'
    )

    # If question image exists and answers do not have images
    if image_url and not has_image_answers:
        messages.append(
            {'type': 'photo', 'content': image_url, 'caption': message_text})
    else:
        messages.append({'type': 'text', 'content': message_text})

    # If answers have images, we return them separately
    if has_image_answers:
        for ans in answers:
            if ans.get('image_url'):
                image_answers.append({
                    'content': ans['image_url'],
                    'caption': ans['text'],
                    'callback_data': f'answer_{question_id}_{ans["id"]}'
                })
        # Return no inline keyboard, because each answer will have its own button
        return messages, image_answers, None

    # Otherwise, create inline buttons for text answers
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            ans['text'],
            callback_data=f'answer_{question_id}_{ans["id"]}'
        )]
        for ans in answers
    ])

    return messages, [], reply_markup
