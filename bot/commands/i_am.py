import json
import re

import requests
from telegram import InlineKeyboardButton, ReplyKeyboardMarkup
from telegram.ext.conversationhandler import ConversationHandler

from commands.books import show_book_actions
from config import API_BASE_URL


class State:
    SAVE_NAME = 2


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
