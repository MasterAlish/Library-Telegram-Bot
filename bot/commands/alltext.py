from bot_core.router import process_text_message
from commands.books import search_books
from commands.text.funny import say_my_name, aaaa


text_patterns = [
    ("[Сс]кажи (?P<name>.*)", say_my_name),
    ("[Нн]айди книг[иу] (?P<keyword>.*)", search_books),
    ("[Аа]+", aaaa)
]


def handle_command(bot, update):
    user_id = update.effective_user.id
    print("User: %d" % user_id)
    if update.effective_chat:
        print("Group: %d" % update.effective_chat.id)

    processed = process_text_message(bot, update, text_patterns)
    if not processed:
        bot.send_message(chat_id=update.message.chat_id, text="Что что?")
