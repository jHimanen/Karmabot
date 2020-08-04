from telegram.ext import Updater, CommandHandler
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

updater = Updater(token="TOKEN", use_context=True)
dispatcher = updater.dispatcher

def start(update, context):{
    context.bot.send_message(chat_id=update.effective_chat_id, text="I bring the karma.")
}

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()
