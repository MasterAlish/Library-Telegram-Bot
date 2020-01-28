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


def handle_command(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Привет, %s! Давайте зарегистрируемся? Нажмите - /iam." % update.effective_user.first_name)
