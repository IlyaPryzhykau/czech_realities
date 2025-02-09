from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants_cz import RESULTS_TEXT, BUTTON_MAIN_MENU


async def show_results(query, context):
    """
    Shows the final results after user completes
    all questions in a ticket or topic.
    """
    correct = context.user_data.get('correct_answers', 0)
    total = context.user_data.get('total_questions', 0)

    result_text = RESULTS_TEXT.format(correct=correct, total=total)

    options = [
        [InlineKeyboardButton(BUTTON_MAIN_MENU, callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(options)

    await query.message.reply_text(
        result_text,
        parse_mode='HTML',
        reply_markup=reply_markup
    )
