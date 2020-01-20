from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import json
import requests
from config import API_BASE_URL


def get_users_from_api(user_data):
    response = user_data.GET.get(API_BASE_URL + "api/search_books/")
    if response.status_code == 200:
        user_data = json.loads(response.text)["users"]
    return []


def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


def handle_command(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Здравствуйте! Я бот BeeLibrary! Введите пожалуйста ФИО")
