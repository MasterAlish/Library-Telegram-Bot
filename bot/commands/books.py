from telegram import ReplyKeyboardMarkup
from telegram.ext.conversationhandler import ConversationHandler

from api.books import Api


def show_book_actions(update):
    reply_keyboard = [['Поиск книги', 'Взять книгу', 'Вернуть книгу']]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text('Выберите действие', reply_markup=keyboard_markup)


def show_yes_no(text, update):
    reply_keyboard = [['Да', 'Нет']]
    keyboard_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(text, reply_markup=keyboard_markup)


class States:
    FIND_BOOKS = 2
    REGISTER_BOOK_TAKING = 3
    CONFIRM_BOOK_TAKING = 4
    RETURN_BOOK_TAKING = 5
    CONFIRM_BOOK_RETURN = 6


def search_book_init(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Введите ключевые слова для поиска книги:")
    return States.FIND_BOOKS


def search_books(update, context):
    keyword = update.message.text
    books = Api.get_books_from_api(keyword)

    books_list = [
        f"{book['id']}. {book['name']}: {book['author']}"
        for book in books
    ]
    books_str = "\n".join(books_list)
    if len(books):
        message = f"По ключевому слову '{keyword}' найдены следующие книги:\n" + books_str
        context.bot.send_message(chat_id=update.message.chat_id, text=message)
    else:
        message = f"По ключевому слову '{keyword}' ничего не найдено\n"
        context.bot.send_message(chat_id=update.message.chat_id, text=message)

    context.user_data['keyword'] = keyword
    show_book_actions(update)
    return ConversationHandler.END


def take_book_init(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="Введите номер книги чтобы зарегистрировать ее на вас:")
    return States.REGISTER_BOOK_TAKING


def register_taking_book(update, context):
    try:
        book_id = int(update.message.text)
        book = Api.find_book_by_id(book_id)
        if book:
            show_yes_no(f"Вы хотите взять книгу \"{book['name']}\"", update)
            context.user_data["book_id_to_take"] = book_id
            return States.CONFIRM_BOOK_TAKING
        else:
            context.bot.send_message(chat_id=update.message.chat_id, text="Книга с таким номером не найдена")
            show_book_actions(update)
            return ConversationHandler.END
    except Exception as e:
        print(e)
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Введите номер книги правильно или нажмите /cancel")
        return States.REGISTER_BOOK_TAKING


def confirm_taking_book(update, context):
    answer = update.message.text
    if answer == 'Да':
        book_id = context.user_data["book_id_to_take"]
        success = Api.register_book_taking(book_id, update.effective_user.id)
        if success:
            context.bot.send_message(chat_id=update.message.chat_id, text="Книга успешно зарегистрирована на вас")
        else:
            context.bot.send_message(chat_id=update.message.chat_id, text="Не удалось зарегистрировать книгу")
        return ConversationHandler.END
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text="Ну ок")
        show_book_actions(update)
        return ConversationHandler.END


def return_book_init(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="Введите номер книги для ее возврата:")
    return States.RETURN_BOOK_TAKING


def return_book(update, context):
    try:
        book_id = int(update.message.text)
        book = Api.find_book_by_id(book_id)
        if book:
            show_yes_no(f"Вы хотите вернуть книгу \"{book['name']}\"", update)
            context.user_data["book_id_to_take"] = book_id
            return States.CONFIRM_BOOK_RETURN
        else:
            context.bot.send_message(chat_id=update.message.chat_id, text="Книга с таким номером не найдена")
            show_book_actions(update)
            return ConversationHandler.END
    except Exception as e:
        print(e)
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Введите номер книги правильно или нажмите /cancel")
        return States.RETURN_BOOK_TAKING


def confirm_return_book(update, context):
    answer = update.message.text
    if answer == 'Да':
        book_id = context.user_data["book_id_to_take"]
        success = Api.register_return_book(book_id, update.effective_user.id)
        if success:
            context.bot.send_message(chat_id=update.message.chat_id, text="Вы успешно вернули книгу")
        else:
            context.bot.send_message(chat_id=update.message.chat_id, text="Не удалось вернуть книгу")
        return ConversationHandler.END
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text="Ну ок")
        show_book_actions(update)
        return ConversationHandler.END
