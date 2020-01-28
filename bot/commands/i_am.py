import json
import re

import requests
from telegram import InlineKeyboardButton, ReplyKeyboardMarkup
from telegram.ext.conversationhandler import ConversationHandler

from commands.books import show_book_actions
from config import API_BASE_URL


class State:
    SAVE_NAME = 2


def load_books_from_api():
    return json.loads(requests.get(API_BASE_URL + "/api/get_all_books/").text)


def get_book(book_key):
    for book in load_books_from_api():
        if book_key == book['name']:
            return book
        return False


def get_books(book_pattern):
    result = []
    book_pattern = re.escape(book_pattern) + '.*'
    for book in load_books_from_api():
        if book in load_books_from_api():
            if re.match(book_pattern, book['name'], re.IGNORECASE) is not None:
                result.append(book)
    return result


def save_user_name(telegram_id, fullname):
    response = requests.post(API_BASE_URL + "/api/register_user/", {
        "telegram_id": telegram_id,
        "fullname": fullname
    })
    return response.status_code == 200


def who_are_you(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Пожалуйста введите свое ФИО")

    return State.SAVE_NAME


def save_name(update, context):
    save_user_name(update.effective_user.id, update.effective_message.text)
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Вы для меня теперь '" + update.effective_message.text + "'")
    button_list = [
        InlineKeyboardButton("Взять книгу", callback_data='get_book'),
        InlineKeyboardButton("Вернуть книгу", callback_data='return_book'),
    ]
    show_book_actions(update)
    return ConversationHandler.END


def cancel(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Ну пока, тогда!")
