from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from telegram.ext.dispatcher import run_async

from time import sleep
from dateutil import parser
import datetime
import re
import pickle
import logging
from Keys import BOTNAME, TOKEN


pinned = []
delay_mess_start = "Thanks for your question $firstname, we will get right back to you."

delay_messages_start = "Thanks for your questions, we will get right back to you."

reminder = "Welcome everyone! Don’t forget to visit our main site dmc.darcmatter.com " \
           "and email DMCICO@darcmatter.com to access the private presale. Latest content " \
           "on https://medium.com/@DarcMatter Have a great day!"
chat = 0
planer = []

questions = {}
pre_q = {}

root = logging.getLogger()
root.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)


@run_async
def send_async(bot, *args, **kwargs):
    logger.info('Try send message')
    global planer
    if kwargs.get('delay'):
        if kwargs.get('delay') < 0:
            logger.info('send_async: time in last')
            planer.remove({"Mes": kwargs.get("text"), "Time": kwargs.get('date_send')})
            return
        sleep(kwargs['delay'])
    bot.sendMessage(*args, **kwargs)
    if kwargs.get('plan'):
        planer.remove({"Mes": kwargs.get("text"), "Time": kwargs.get('date_send')})


"""
@run_async
def pin_async(bot, *args, **kwargs):
    if kwargs.get('delay'):
        sleep(kwargs['delay'])
    mess = bot.sendMessage(*args, **kwargs)
    bot.pinChatMessage(chat_id=kwargs['chat_id'], message_id=mess.message_id)
"""


@run_async
def delay_async(bot, *args, **kwargs):
    logger.info('Come question')
    # 15 min
    sleep(15)
    global pre_q
    if kwargs["mess_id"] in pre_q.keys():
        if len({el["Author"].first_name for el in pre_q.values()}) > 1:
            kwargs["text"] = delay_messages_start
        bot.sendMessage(*args, **kwargs)
        questions.update(pre_q)
        pre_q = {}
    else:
        logger.info("There's an answer")


@run_async
def remind_helper(bot, *args, **kwargs):
    while 1:
        try:
            remind_async(bot, *args, **kwargs)
        except:
            logger.info("Remind error")
            sleep(2)


def remind_async(bot, *args, **kwargs):
    time_1 = datetime.time(3, 0, 0)  # Напоминалка в 10 утра
    time_2 = datetime.time(19, 0, 0)  # и в 5 вечера
    time_now = datetime.datetime.now().time()
    delay_1 = (time_1.hour - time_now.hour) * 60 * 60 + \
              (time_1.minute - time_now.minute) * 60 + \
              (time_1.second - time_now.second)
    delay_2 = (time_2.hour - time_now.hour) * 60 * 60 + \
              (time_2.minute - time_now.minute) * 60 + \
              (time_2.second - time_now.second)
    if delay_2 < 0 and delay_1 < 0:
        delay_2 += 86400
        delay_1 += 86400
    if delay_1 < 0:
        delay_ = delay_2
    elif delay_2 < 0:
        delay_ = delay_1
    else:
        delay_ = delay_1 if delay_1 < delay_2 else delay_2
    sleep(delay_)
    bot.sendMessage(text=reminder, *args, **kwargs)
    logger.info("Send remind message")
    sleep(2)


# Welcome a user to the chat
def welcome(bot, update):
    message = update.message
    chat_id = message.chat.id
    # Приветственный текст
    #text = "Hello, %s! Welcome to the DarcMatter Telegram chat!" % (message.new_chat_member.first_name,)
    logger.info("Welcome new user")
    #send_async(bot, chat_id=chat_id, text=text, parse_mode=ParseMode.HTML)


def introduce(bot, update):
    global chat
    # Текст для админов с обьяснением функций
    text_for_admin = "Hello! I'm %s bot. \n You can control me with commands:\n" \
                     "/plan yyyy-mm-dd hh:mm, msg - write message in group\n" \
                     "/remind msg - change the text of regular message (in 3 a.m and 7 p.m)\n" \
                     "/delay msg - change the response to unanswered messages\n" \
                     "/q - list of unanswered messages\n" \
                     "/answ ID1, ID2,.., IDN; msg - give an answer\n\n" \
                     "For example: \n/plan 2018-01-31 11:00, Hello! How are you?\n" \
                     "/remind Visit our site\n" \
                     "/delay We will contact you soon $firstname\n" \
                     "/answ 345, 346; answer\n" % \
                     (BOTNAME,)
    chat_id = update.message.chat.id
    if chat_id == chat:
        send_async(bot, chat_id=update.message.from_user.id, text="Bot already connected")
        return

    if chat_id > 0:
        if chat_id in admins(bot, chat_id):
            text = text_for_admin
            logger.info('Introduce for admin')
        else:
            text = "You can't control me"
            logger.info('Introduce for not admin')
    else:
        if chat == 0:
            logger.info('Introduce in new chat')
            chat = chat_id
            with open('id.pickle', 'wb') as f:
                pickle.dump(chat, f)
            init(bot)
        if chat != chat_id:
            logger.info('Introduce in other chat')
            send_async(bot, chat_id=chat_id, text="Error")
            return
        for el in admins(bot, chat_id):
            send_async(bot, chat_id=el, text=text_for_admin)
        # Бот представляет себя в чате
        text = ""

    if text:
        send_async(bot, chat_id=chat_id, text=text)


def empty_message(bot, update):
    logger.info('Get empty message')
    if update.message.new_chat_members is not None:
        if update.message.new_chat_members[0] == bot.get_me():
            return introduce(bot, update)
        else:
            return welcome(bot, update)


"""
def pin(bot, update):
    chat_id = update.message.chat.id
    if chat_id > 0 and chat_id in admins(bot):
        delay_, date, mess = parse(update.message.text[4:])
        res = "message: %s\nTime: %s" % (mess, date)
        send_async(bot, chat_id=chat_id, text=res)
        pin_async(bot, chat_id=admins[chat_id], text=mess, delay=delay_)
"""


def plan(bot, update):
    chat_id = update.message.chat.id
    if chat_id > 0 and chat_id in admins(bot, chat):
        logger.info('Plan created')
        delay_, date, mess = parse(update.message.text[5:])
        res = "Message: %s\nTime: %s" % (mess, date)
        planer.append({"Mes": mess.strip(), "Time": date})
        send_async(bot, chat_id=chat_id, text=res)
        send_async(bot, chat_id=chat, text=mess.strip(), delay=delay_, date_send=date, plan=True)
    else:
        logger.info('Plan access error')


def remind(bot, update):
    chat_id = update.message.chat.id
    if chat_id > 0 and chat_id in admins(bot, chat):
        logger.info('Remind changed')
        global reminder
        reminder = update.message.text[7:]
        res = "Message was changed to \n'%s'" % (reminder,)
        send_async(bot, chat_id=update.message.chat.id, text=res)
    else:
        logger.info('Remind access error')


def delay(bot, update):
    chat_id = update.message.chat.id
    if chat_id > 0 and chat_id in admins(bot, chat):
        logger.info('Delay answer changed')
        global delay_mess_start
        delay_mess_start = update.message.text[6:]
        res = "Message was changed to \n'%s'" % (delay_mess_start,)
        send_async(bot, chat_id=update.message.chat.id, text=res)
    else:
        logger.info('Delay answer: access error')


def get_questions(bot, update):
    chat_id = update.message.chat.id
    if chat_id > 0 and chat_id in admins(bot, chat):
        logger.info('Admin get questions')
        res = ["ID: %s\nAuthor: %s\nTime: %s\nMessage: %s"
               % (k, el["Author"].first_name, el["Time"], el["Message"]) for (k, el) in questions.items()]
        res = "\n------------\n".join(res) if res else "list is empty"
        results = [res[i:i+4000] for i in range(0, len(res), 4000)]
        for mes in results:
            sleep(1)
            send_async(bot, chat_id=chat_id, text=mes)
    else:
        logger.info('Get questions: access error')


def start(bot, update):
    chat_id = update.message.chat.id
    if update.message.from_user.id in admins(bot, chat_id):
        introduce(bot, update)
    else:
        logger.info('Start not admin')


def do_answer(bot, update):
    chat_id = update.message.chat.id
    if chat_id > 0 and chat_id in admins(bot, chat):
        logger.info('Admin do answer')
        mess = update.message.text[5:].strip()
        parse_data = mess.split(";")
        if len(parse_data) < 2:
            send_async(bot, chat_id=chat_id, text="Wrong format")
            return
        if len(parse_data) > 2:
            text = ";".join(parse_data[1:])
            parse_data = [parse_data[0], text]
        mess_id, answ = parse_data
        nums = re.search(r"^\d+(, \d+)*$", mess_id)
        if not nums:
            send_async(bot, chat_id=chat_id, text="Wrong id format")
            return
        nums = re.findall(r"\d+", nums.group(0))
        ids = []
        for el in nums:
            try:
                num = int(el)
            except:
                send_async(bot, chat_id=chat_id, text="error with %s id" % (el,))
            else:
                ids.append(num)
        if answ.strip() == "del":
            for el in ids:
                if questions.get(el):
                    del questions[el]
                else:
                    send_async(bot, chat_id=chat_id, text="Can't delete %d message" % (el,))
            send_async(bot, chat_id=chat_id, text="Deleted")
            return
        u_names = set()
        for el in ids:
            if questions.get(el) and questions.get(el).get("Author"):
                if questions.get(el).get("Author").username:
                    u_names.update({"@" + questions.get(el).get("Author").username})
                elif questions.get(el).get("Author").first_name:
                    u_names.update({questions.get(el).get("Author").first_name})
        send_async(bot, chat_id=chat, text=", ".join(u_names) + ", " + answ)
        for el in ids:
            if questions.get(el):
                del questions[el]
            else:
                send_async(bot, chat_id=chat_id, text="Can't delete %d message" % (el,))
        send_async(bot, chat_id=chat_id, text="Ok")
    else:
        logger.info('Answer: access error')


def ask(bot, update):
    chat_id = update.message.chat.id
    if chat_id != chat:
        return
    mess = update.message.text
    user = update.message.from_user
    ent = update.message.entities
    if user.id in admins(bot, chat):
        logger.info('Message from admin')
        global pre_q
        pre_q= {}
    elif isAsk(mess.lower()):
        mess_without_url = mess
        if "url" in [el.type for el in ent]:
            mess_without_url = re.split(r"https?://", mess)[0]
        if not isAsk(mess_without_url.lower()):
            logger.info('url in chat')
            return
        logger.info('Ask in chat')
        pre_q[update.message.message_id] = {"Message": mess, "Author": user, "Time": update.message.date}
        delay_async(bot, chat_id=chat_id, mess_id=update.message.message_id,
                    text=beutify(delay_mess_start, user))
    else:
        logger.info('Message from user')


def get_bots(bot, update):
    chat_id = update.message.chat.id
    if chat_id > 0 and chat_id in admins(bot, chat):
        logger.info('Admin get bots')
        mes = ""
        #users = getFullChat()
        print(chat)
        send_async(bot, chat_id=chat_id, text=mes)
    else:
        logger.info('Get bots: access error')


def admins(bot, chat_id):
    admns = []
    for el in bot.getChatAdministrators(chat_id):
        admns.append(el.user.id)
    return admns


def isAsk(txt):
    if re.match(r".*((\?)|when|(why)|(who)|(where)|(what)|(which)|(how)).*", txt):
        return True
    return False


def parse(txt):
    split = txt.find(',')
    date = txt[:split]
    mess = txt[split + 1:]
    datet = parser.parse(date)
    d = datet - datetime.datetime.now()
    d = d.days * 86400 + d.seconds
    return d, datet, mess


def save(bot, update):
    logger.info('Save')
    with open('data.pickle', 'wb') as f:
        pickle.dump(planer, f)
    with open('questions.pickle', 'wb') as f:
        pickle.dump(questions, f)
    chat_id = update.message.chat.id
    send_async(bot, chat_id=chat_id, text="Saved")


def load_data():
    global planer
    global questions
    try:
        with open('data.pickle', 'rb') as f:
            planer = pickle.load(f)
    except:
        logger.info('plan data do not loaded')
    try:
        with open('questions.pickle', 'rb') as f:
            questions = pickle.load(f)
    except:
        logger.info('questions do not loaded')


def beutify(txt, user):
    if user.username:
        txt = txt.replace("$username", user.username)
    if user.first_name:
        txt = txt.replace("$firstname", user.first_name)
    if user.last_name:
        txt = txt.replace("$lastname", user.last_name)
    return txt


def error_callback(bot, update, error):
    pass


def init(bot):
    try:
        load_data()
    except:
        logger.info("Load error")
    else:
        logger.info("Plan data loaded")

    remind_helper(bot, chat_id=chat)
    for el in planer:
        delay_, date, mess = parse("%s, %s" % (el['Time'], el["Mes"]))
        send_async(bot, chat_id=chat, text=mess.strip(), delay=delay_, date_send=date, plan=True)


def main(ch =0):
    global chat
    chat = ch

    updater = Updater(TOKEN, workers=10)
    if ch != 0:
        init(updater.bot)
    dp = updater.dispatcher

    # dp.add_handler(CommandHandler("pin", pin))
    dp.add_handler(CommandHandler("plan", plan))
    dp.add_handler(CommandHandler("remind", remind))
    dp.add_handler(CommandHandler("delay", delay))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("save", save))
    dp.add_handler(CommandHandler("q", get_questions))
    dp.add_handler(CommandHandler("answ", do_answer))
    dp.add_handler(CommandHandler("bot_list", get_bots))
    dp.add_handler(MessageHandler(Filters.status_update, empty_message))
    #dp.add_handler(MessageHandler(Filters.all, ask))
    dp.add_error_handler(error_callback)

    updater.start_polling(timeout=30, clean=False)

    updater.idle()


if __name__ == '__main__':
    try:
        ch = input("Do you want to connect to the old chat [y|n] ")
    except:
        logger.info('Not connected')
        main()
    else:
        if ch.strip() == 'y':
            try:
                with open('id.pickle', 'rb') as f:
                    ch_id = pickle.load(f)
            except:
                logger.info('id chat do not loaded')
                main()
            else:
                main(ch_id)
        else:
            main()

