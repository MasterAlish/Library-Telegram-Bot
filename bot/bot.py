import logging
import schedule
import time
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram.ext.dictpersistence import DictPersistence

from commands import start, alltext, i_am, books
from config import API_TOKEN
from filters import TextFilter

updater = Updater(token=API_TOKEN, use_context=True, persistence=DictPersistence())
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

dispatcher.add_handler(CommandHandler('start', start.handle_command))

who_are_you_handler = ConversationHandler(
    entry_points=[CommandHandler('iam', i_am.who_are_you)],
    states={
        i_am.State.SAVE_NAME: [MessageHandler(Filters.text, i_am.save_name)],
    },
    fallbacks=[[CommandHandler('cancel', i_am.cancel)]],
)
dispatcher.add_handler(who_are_you_handler)

search_books_handler = ConversationHandler(
    entry_points=[MessageHandler(TextFilter("Поиск книги"), books.search_book_init)],
    states={
        books.States.FIND_BOOKS: [MessageHandler(Filters.text, books.search_books)],
    },
    fallbacks=[[CommandHandler('cancel', i_am.cancel)]], persistent=True, name="Search Books"
)
dispatcher.add_handler(search_books_handler)

search_books_handler = ConversationHandler(
    entry_points=[MessageHandler(TextFilter("Взять книгу"), books.take_book_init)],
    states={
        books.States.REGISTER_BOOK_TAKING: [MessageHandler(Filters.text, books.register_taking_book)],
        books.States.CONFIRM_BOOK_TAKING: [MessageHandler(Filters.text, books.confirm_taking_book)],
    },
    fallbacks=[[CommandHandler('cancel', i_am.cancel)]], persistent=True, name="Search Books"
)
dispatcher.add_handler(search_books_handler)


search_books_handler = ConversationHandler(
    entry_points=[MessageHandler(TextFilter("Вернуть книгу"), books.return_book_init)],
    states={
        books.States.RETURN_BOOK_TAKING: [MessageHandler(Filters.text, books.return_book)],
        books.States.CONFIRM_BOOK_RETURN: [MessageHandler(Filters.text, books.confirm_return_book)],
    },
    fallbacks=[[CommandHandler('cancel', i_am.cancel)]], persistent=True, name="Search Books"
)
dispatcher.add_handler(search_books_handler)


dispatcher.add_handler(MessageHandler(Filters.text, alltext.handle_command))

updater.start_polling()
updater.idle()