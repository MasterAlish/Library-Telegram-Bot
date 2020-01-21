import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

from commands import start, alltext, i_am
from config import API_TOKEN

updater = Updater(token=API_TOKEN)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

dispatcher.add_handler(CommandHandler('start', start.handle_command))

who_are_you_handler = ConversationHandler(
    entry_points=[CommandHandler('iam', i_am.who_are_you)],
    states={
        i_am.State.SAVE_NAME: [MessageHandler(Filters.text, i_am.save_name)],
    },
    fallbacks=[[CommandHandler('cancel', i_am.cancel)]]
)

dispatcher.add_handler(who_are_you_handler)

dispatcher.add_handler(MessageHandler(Filters.text, alltext.handle_command))

updater.start_polling()
updater.idle()
