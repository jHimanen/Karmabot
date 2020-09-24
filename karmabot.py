from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, PicklePersistence
import logging
import os

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def get_token():
    with open('token', 'r') as f:
        token = f.readline()
        token = token.strip()
        return token

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I bring the karma.")

def addKarma(update, context):
    args = context.args
    if len(args) == 2:
        user = args[0]
        amount = int(args[1])
        old_karma = context.chat_data[user] if (user in context.chat_data) else 0
        new_karma = old_karma + abs(amount)
        context.chat_data[user] = new_karma
        context.bot.send_message(chat_id=update.effective_chat.id, text="Added {} karma to {}. New total karma: {}".format(amount, user, new_karma))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Usage: /addKarma [user] [amount]")

def removeKarma(update, context):
    args = context.args
    if len(args) == 2:
        user = args[0]
        amount = int(args[1])
        old_karma = context.chat_data[user] if (user in context.chat_data) else 0
        new_karma = old_karma - abs(amount)
        context.chat_data[user] = new_karma
        context.bot.send_message(chat_id=update.effective_chat.id, text="Removed {} karma from {}. New total karma: {}".format(amount, user, new_karma))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Usage: /removeKarma [user] [amount]")

def modifyKarma(update, context):
    args = context.args
    if len(args) == 2:
        user = args[0]
        amount = int(args[1])
        if amount < 0:
            removeKarma(update, context)
        else:
            addKarma(update, context)

    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Usage: /modifyKarma [user] [amount]")

# Vois ton dictin rakenteen muuttaa context.chat_data['karma'][user]
# Jos haluu joskus muutaki ku käyttäjien karmat sinne
def karmaList(update, context):
    text = "Total karma for each user: \n"
    for key in context.chat_data:
        text += "{}: {}\n".format(key, context.chat_data[key])
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

def removeFromList(update, context):
    if len(context.args) == 1:
        user = context.args[0]
        if user in context.chat_data:
            del context.chat_data[user]
            context.bot.send_message(chat_id=update.effective_chat.id, text="{} removed from karma list".format(user))
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="No user named {} found in karma list".format(user))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Usage: /removeFromList [user]")

def main():
    print("STARTING BOT")
    pp = PicklePersistence(filename='karmabotpickle')
    updater = Updater(token=get_token(), persistence=pp, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    addKarma_handler = CommandHandler('addKarma', addKarma)
    removeKarma_handler = CommandHandler('removeKarma', removeKarma)
    modifyKarma_handler = CommandHandler('modifyKarma', modifyKarma)
    karmaList_handler = CommandHandler('karmaList', karmaList)
    removeFromList_handler = CommandHandler('removeFromList', removeFromList)
    
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(addKarma_handler)
    dispatcher.add_handler(removeKarma_handler)
    dispatcher.add_handler(modifyKarma_handler)
    dispatcher.add_handler(karmaList_handler)
    dispatcher.add_handler(removeFromList_handler)


    updater.start_polling()

    print("BOT STARTED")

    updater.idle()

if __name__== "__main__":
    main()
