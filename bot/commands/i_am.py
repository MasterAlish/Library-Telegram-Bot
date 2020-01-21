import json

import requests
from telegram.ext.conversationhandler import ConversationHandler

from config import API_BASE_URL


class State:
    SAVE_NAME = 2


def save_user_name(telegram_id, fullname):
    response = requests.post(API_BASE_URL + "/api/register_user/", {
        "telegram_id": telegram_id,
        "fullname": fullname
    })
    return response.status_code == 200


def who_are_you(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Пожалуйста введите свое ФИО")

    return State.SAVE_NAME


def save_name(bot, update):
    save_user_name(update.effective_user.id, update.effective_message.text)

    bot.send_message(
        chat_id=update.message.chat_id,
        text="Вы для меня теперь '" + update.effective_message.text + "'")

    return ConversationHandler.END


def cancel(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Ну пока, тогда!")
