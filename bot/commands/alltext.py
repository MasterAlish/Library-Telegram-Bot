from bot_core.router import process_text_message
from commands.text.funny import say_my_name, aaaa

text_patterns = [
    ("[Сс]кажи (?P<name>.*)", say_my_name),
    ("[Аа]+", aaaa)
]


def handle_command(update, context):
    user_id = update.effective_user.id
    print("User: %d" % user_id)
    if update.effective_chat:
        print("Group: %d" % update.effective_chat.id)

    processed = process_text_message(context.bot, update, text_patterns)
    if not processed:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Не знаю такую команду :) Ниже прилагаю список доступных команд: \n 1. Поиск книги \n 2. Вернуть книгу \n 3. Вернуть книгу \n 4. /cancel")