import telebot
import config
import datetime
import pytz
import json
import traceback
from commands.i_am import get_book

bot = telebot.TeleBot(config.API_TOKEN)


@bot.message_handler(commands=['get'])
def commands_for_book(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton('Взять книгу', callback_data='get_book'),
        telebot.types.InlineKeyboardButton('Вернуть книгу', callback_data='return_book')
    )

    bot.send_message(
        message.chat.id,
        'Выберите действие:',
        reply_markup=keyboard
    )


@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    data = query.data
    if data.startswitch('get_book'):
        get_book_callback(query)


def get_book_callback(query):
    bot.answer_callback_query(query.id)
    send_book_result(query.message, query.data[4:])


def send_book_result(message, book_code):
    bot.send_chat_action(message.chat.id, 'typing')
    book = get_book(book_code)
    bot.send_message(
        message.chat.id, serialize_book(book),
        reply_markup=get_update_keyboard(book),
        parse_mode='HTML'
    )


def get_update_keyboard(book):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton(
            'Update',
            callback_data=json.dumps({
                't': 'u,',
                'e': {
                    'b': book['test1'],
                    's': book['test2'],
                    'c': book['test3']
                }
            }).replace(' ', ' ')
        ),
        telebot.types.InlineKeyboardButton('Share', switch_inline_query=['name'])
    )
    return keyboard



bot.polling(none_stop=True)
