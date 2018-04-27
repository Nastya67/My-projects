from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackQueryHandler
from telegram.ext.dispatcher import run_async
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

from time import sleep
from dateutil import parser
import datetime
import re
import pickle
import logging
import botClass
from Keys import BOTNAME, TOKEN 


root = logging.getLogger()
root.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)


@run_async
def send_async(bot, *args, **kwargs):
    logger.info('Try send message')
    bot.sendMessage(*args, **kwargs)


def start(bot, update):

    text = "Hi $firstname! I’m your friendly DarcMatter Bounty Bot. We have just finished " \
           "the latest round of airdrops, but will have more opportunities coming up soon! " \
           "In the meantime, you may update your NEM address or check your airdrop balance."

    logger.info('Start')
    keyboard = [[InlineKeyboardButton("Join our Telegram Group", url="https://t.me/DarcMatter", callback_data='0')],
                [InlineKeyboardButton("Submit Details", callback_data='1')],
                [InlineKeyboardButton("Check Airdrop Balance", callback_data='2')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    # update.message.reply_text('Please choose:', reply_markup=reply_markup)
    send_async(bot, chat_id=update.message.chat.id, text=beutify(text, update.message.from_user),
               reply_markup=reply_markup)
    db = botClass.User()
    db.add_user(update.message.from_user)
    db.con_close()


def join(bot, update):
    print("join")


def check(bot, mess):
    text = "Thank you for participating in the DarcMatter Airdrop! \n\nYou have a total of 0 DMC " \
           "tokens. Keep on going and invite more friends! \n\nPlease remember that you have to stay " \
           "in our chat to earn the tokens. We will verify that you have followed us on the respective " \
           "channels before the DMC tokens will be distributed to you. \n\nGo back to /menu"
    send_async(bot, chat_id=mess.chat.id, text=beutify(text, mess.from_user))


def settings(bot, update):
    sett(bot, update.message.chat.id)


def sett(bot, mess):
    text = "Submit your details for us to verify your participation in our campaign."

    custom_keyboard = [['Submit NEM Address', 'Submit Twitter Username'],
                       ['Submit Medium Email', 'Submit Email Address'],
                       ["Close"]]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    send_async(bot, chat_id=mess.chat.id, text=text, reply_markup=reply_markup)


def set_NEM(bot, update):
    text = "Submit your NEM address so that we can credit your bounty tokens. \n\n" \
           "Don't have one? Check out this guide - j.mp/NEMWalletGuide An alternative " \
           "would be to use @NEMWalletCreatorBot."
    send_async(bot, chat_id=update.message.chat.id, text=text)
    global status

    def save_NEM(user, nem):
        db = botClass.User()
        db.update_NEM(user, nem)
        db.con_close()
        return True
    status.save_info = save_NEM


def set_med(bot, update):
    text = "Submit your Medium email address so that we can verify you followed us on Medium."
    send_async(bot, chat_id=update.message.chat.id, text=text)
    global status

    def save_med(user, med):
        db = botClass.User()
        db.update_med(user, med)
        db.con_close()
        return True
    status.save_info = save_med


def set_email(bot, update):
    text = "Submit your email address to receive news about DarcMatter and our partners, " \
           "and updates on future Bounty AirDrops!"
    send_async(bot, chat_id=update.message.chat.id, text=text)
    global status

    def save_email(user, em):
        db = botClass.User()
        db.update_email(user, em)
        db.con_close()
        return True
    status.save_info = save_email


def set_twitter(bot, update):
    text = "Submit your Twitter username in the format @username so that we can verify you followed us."
    send_async(bot, chat_id=update.message.chat.id, text=text)
    global status

    def save_twit(user, tw):
        db = botClass.User()
        db.update_twit(user, tw)
        db.con_close()
        return True

    status.save_info = save_twit


def set_close(bot, update):
    text = " Submitting closed."
    reply_markup = ReplyKeyboardRemove()
    send_async(bot, chat_id=update.message.chat.id, text=text, reply_markup=reply_markup)
    global status

    def idle(user, idle):
        pass
    status.save_info = idle


def button(bot, update):
    query = update.callback_query
    shadule[int(query.data)](bot, query.message)


def text_filter(bot, update):
    text = update.message.text
    if text_filter_list.get(text):
        text_filter_list[text](bot, update)
    else:
        if status.save_info:
            if status.save_info(update.message.from_user, update.message.text):
                send_async(bot, chat_id=update.message.chat.id, text="ok")
                status.save_info = None


def beutify(txt, user):
    if user.username:
        txt = txt.replace("$username", user.username)
    if user.first_name:
        txt = txt.replace("$firstname", user.first_name)
    if user.last_name:
        txt = txt.replace("$lastname", user.last_name)
    return txt


def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def error_callback(bot, update, error):
    logger.info(error)


def main():
    updater = Updater(TOKEN, workers=10)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("menu", start))
    dp.add_handler(CommandHandler("join", join))
    dp.add_handler(CommandHandler("check", check))
    dp.add_handler(CommandHandler("set", settings))
    dp.add_handler(MessageHandler(Filters.text, text_filter))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    dp.add_error_handler(error_callback)

    updater.start_polling(timeout=30, clean=False)

    updater.idle()


status = botClass.Status(None)
shadule = [join, sett, check]
text_filter_list = {"Submit NEM Address": set_NEM,
                    "Submit Twitter Username": set_twitter,
                    'Submit Medium Email': set_med,
                    'Submit Email Address': set_email,
                    "Close": set_close}


if __name__ == '__main__':
    main()
