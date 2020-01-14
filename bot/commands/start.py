from telegram import InlineKeyboardButton, InlineKeyboardMarkup


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
    user_id = update.effective_user.id
    # bot.send_message(chat_id=update.message.chat_id, text="Здравствуйте, я бот BeeLibrary")

    button_list = [
        InlineKeyboardButton("col1", callback_data=213),
        InlineKeyboardButton("col2", callback_data=213),
        InlineKeyboardButton("row 2", callback_data=213)
    ]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    bot.send_message(chat_id=update.message.chat_id, text="A two-column menu", reply_markup=reply_markup, parse_mode='HTML')
