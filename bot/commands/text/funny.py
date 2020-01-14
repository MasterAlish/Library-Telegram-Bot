def aaaa(bot, update, **kwargs):
    bot.send_message(chat_id=update.message.chat_id, text="AaaAAA!")
    return True


def say_my_name(bot, update, **kwargs):
    bot.send_message(chat_id=update.message.chat_id, text=kwargs["name"])
    return True
