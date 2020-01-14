import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from commands import start, alltext
from config import API_TOKEN

updater = Updater(token=API_TOKEN)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

dispatcher.add_handler(CommandHandler('start', start.handle_command))
dispatcher.add_handler(MessageHandler(Filters.all, alltext.handle_command))

updater.start_polling()
updater.idle()
