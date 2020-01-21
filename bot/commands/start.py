def handle_command(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Привет, %s! Чтобы мы познакомились нажмит /iam.\n\nЧем могу помочь?" % update.effective_user.first_name )
