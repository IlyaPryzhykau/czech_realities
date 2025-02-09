"""
This module holds all Czech text constants used by the bot.
Keeping them in one place simplifies localization or text edits.
"""

# Common messages
ERROR_NO_ANSWER = '⚠️ Chyba: Nelze ověřit odpověď.'
ERROR_UNKNOWN_MENU = '❌ Neznámý příkaz menu.'

# Correct/incorrect answer
ANSWER_CORRECT = '✅ <b>Správně!</b>\nOdpověď: {answer}'
ANSWER_INCORRECT = '❌ <b>Nesprávně!</b>\nSprávná odpověď: {answer}'

# Buttons
BUTTON_CONTINUE = '▶️ Pokračovat'
BUTTON_NEXT_QUESTION = '🔄 Další otázka'
BUTTON_MAIN_MENU = '📋 Hlavní menu'
BUTTON_CHOOSE_TOPIC = '📚 Vybrat téma'
BUTTON_RANDOM_QUESTION = '🎲 Náhodná otázka'
BUTTON_RANDOM_TICKET = '🎟 Náhodný testový lístek'
BUTTON_START = '🚀 Start'
BUTTON_HELP = 'ℹ️ Help'
BUTTON_SELECT_ANSWER = '✔️ Vybrat'

# Main menu
MAIN_MENU_TITLE = '🏠 <b>Hlavní menu</b>\n\nVyberte akci:'

# Help texts
HELP_INSTRUCTIONS = (
    '📌 Jak používat bota:\n'
    '1️⃣ Vyberte si téma nebo testový lístek.\n'
    '2️⃣ Odpovídejte na otázky kliknutím na možnosti.\n'
    '3️⃣ Na konci uvidíte výsledek.\n\n'
    '📋 Seznam příkazů:\n'
    '/start - Spustit bota a zobrazit menu\n'
    '/help - Nápověda\n'
)
HELP_CHOOSE_OPTION = '📌 Vyberte možnost:'

# Start texts
START_CHOOSE_OPTION = '📌 Vyberte možnost:'

# Random question / tickets errors
ERROR_NO_QUESTIONS_FOUND = '❌ Nebyly nalezeny žádné otázky.'
ERROR_TICKET_LOAD = '🚫 Nepodařilo se načíst test.'

# Topic messages
CHOOSE_TOPIC_TEXT = 'Vyberte téma:'
ERROR_NO_QUESTIONS_TOPIC = '🚫 Toto téma zatím neobsahuje žádné otázky.'

# Results
RESULTS_TEXT = (
    '🎉 <b>Výsledek testu</b>\n\n'
    '✅ Správné odpovědi: {correct} / {total}\n\n'
)

# --- Below are the large constants you already had in your code ---
WELCOME_TITLE = (
    '<b>📚 Databanka testových úloh z českých reálií</b>\n'
    'Vítejte v databance testových úloh ke zkoušce z českých reálií! '
    '🎓 Tento test je určen pro cizince žádající o české občanství.\n'
)

BOT_FEATURES = (
    '<b>🔹 Co najdete v tomto bota?</b>\n'
    '✅ <b>Výběr tématu</b> – procvičujte otázky z konkrétního tématu.\n'
    '✅ <b>Náhodná otázka</b> – otestujte své znalosti na náhodné otázce.\n'
    '✅ <b>Náhodný testový lístek</b> – vyzkoušejte test složený z otázek '
    'z různých oblastí.\n'
)

TEST_STRUCTURE = (
    '<b>📌 Struktura databanky testových úloh</b>\n'
    'Testové úlohy jsou rozděleny do <b>3 oblastí</b> a celkem <b>30 témat</b>:\n\n'
    '📖 <b>Občanský základ</b> – 16 témat\n'
    '🗺 <b>Základní geografické informace o ČR</b> – 7 témat\n'
    '🏛 <b>Základní historické a kulturní informace o ČR</b> – 7 témat\n\n'
    'Každý test obsahuje otázky ze všech 30 témat, přičemž každé téma je '
    'zastoupeno <b>jednou otázkou</b>.\n'
)

QUESTION_FORMAT = (
    '<b>❓ Jak vypadá otázka?</b>\n'
    '▪ Každá otázka má <b>zadání</b> a <b>4 možné odpovědi</b>.\n'
    '▪ <b>Pouze 1 odpověď</b> je správná, ostatní 3 jsou nesprávné.\n'
    '▪ Zadání může obsahovat <b>text, obrázek, tabulku nebo tvrzení</b>.\n'
    '▪ Pokud se v otázce vyskytuje zápor, je vždy <u>podtržený</u>.\n'
)

IMPORTANT_INFO = (
    '<b>ℹ️ Důležité informace</b>\n'
    '📝 Otázky odpovídají jazykové úrovni <b>B1</b> dle Společného referenčního '
    'rámce pro jazyky.\n'
    '📍 V testových úlohách se může objevit jak <b>„Česká republika“</b>, tak '
    'jednoslovný název <b>„Česko“</b>.\n'
    '👥 Slovo <b>„občan“</b> označuje jak muže, tak ženy s českým občanstvím.\n'
    '📜 Obsah otázek vychází z platné legislativy, včetně <b>nového občanského '
    'zákoníku (zákon č. 89/2012 Sb.)</b>.\n'
    '🔄 <b>Databanka testových úloh je průběžně aktualizována</b> podle změn '
    'v legislativě a reáliích.\n\n'
    '⚡ <b>Začněte trénovat hned teď!</b>\n'
    'Vyberte jednu z možností v menu a otestujte své znalosti. 🏆'
)
