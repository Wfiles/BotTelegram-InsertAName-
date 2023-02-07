import logging
import variables
import os
import random
import telegram
import json

from datetime import datetime
import pytz

from methods.basic import start, recommendations
from methods.troll import rickrolled, ban, sendSticker
from methods.polls import epfl, onmangeou
from methods.spam import storm, kat, doggo, memes, babypic, complimentme, copains, aaa

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

kachow_chat_id = -1878934544 #os.getenv('KACHOW_CHAT_ID')

with open("source/birthdays.json", "r") as f:
    birthdays = json.load(f)
f.close()

PORT = int(os.environ.get('PORT', 5000))
TOKEN = '5862212486:AAFZmdpodJByZPh6GJM5QdY4MLac6-9eePs' #os.getenv('API_TOKEN')
rec_chat_id = os.getenv('RECOMMENDATION_CHAT_ID')

variables.bot = telegram.Bot(token=TOKEN)

# Enable logging
logging.basicConfig(format = "%(asctime)s - %(name)s - %(levelname)s  - %(message)s", level = logging.INFO)

logger = logging.getLogger(__name__)

#error function of the bot
def error(update, context):
    logger.warning(f'Update "{update}" caused error "{context.error}"')

#help function of the bot
def help(update, context):
    number = random.randint(1, 100)
    if number == 5:
        update.message.reply_text(
            """che7 je vais pas t'aider""")
        rickrolled(update, context)
        return
    else :
        update.message.reply_text(
"""here's some info about me :)
/start : starts me,
/help : mdr
/where : creates a poll to see who is where on campus
/ban : ban a friend for the lols
/storm : JAD IS APPROACHING
/kat : sends a cute cat picture :3
/doggo : sends a cute dog picture :>
/babypic : self explanatory :D
/copains : sends a pic of us ;)
/manger : sends a poll to see where we eat
/rec : sends us recommendations about what you want to see, you only need to send the message in the format '/rec blabla' :)
/aaa : AAAAAAAAAAAAAAAAAAAAA
...""")

def birthday(update, context):
    time = datetime.now(pytz.timezone('Europe/Zurich'))
    job_queue = updater.job_queue
    if job_queue.jobs != None:
        return
    for bday in birthdays["birthdays"]:
        job_queue.run_repeating(birthday_message(bday, time), interval = 86400, first = 0.0)

def birthday_message(bday, time):
    age = time.year - int(bday['year'])
    print(bday['year'])
    if (int(bday['year']) <= 2004):
        variables.bot.send_message(
            chat_id = kachow_chat_id,
            text = f'Happy birthday {bday["name"]} ! ur still a baby hehe, only {age} years old >:) we still love you tho ;)')
    elif (int(bday['year']) == 2003):
        variables.bot.send_message(
            chat_id = kachow_chat_id,
            text = f'Happy birthday {bday["name"]} ! {age} ans déjà !!! we love you enjoy it au max ;)')
    else:
        variables.bot.send_message(
            chat_id = kachow_chat_id,
            text = f'Happy birthday {bday["name"]} ! ur old, {age} ans déjà :| jk jk we love you anyway ;)')
    return

##################################################################################
##############################    MAIN    ########################################
##################################################################################


updater = Updater(token = TOKEN, use_context = True)

global dp
dp = updater.dispatcher

#add the function handlers for each function of the bot
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("help", help))
dp.add_handler(CommandHandler("storm", storm))
dp.add_handler(CommandHandler("where", epfl))
dp.add_handler(CommandHandler("rickrolled", rickrolled))
dp.add_handler(CommandHandler("rec", recommendations))
dp.add_handler(CommandHandler("ban", ban))
dp.add_handler(CommandHandler("kat", kat))
dp.add_handler(CommandHandler("doggo", doggo))
#dp.add_handler(CommandHandler("meme", memes))
dp.add_handler(CommandHandler("babypic", babypic))
dp.add_handler(CommandHandler("complimentme", complimentme))
dp.add_handler(CommandHandler("copains", copains))
dp.add_handler(CommandHandler("manger", onmangeou))
dp.add_handler(CommandHandler("aaa", aaa))
dp.add_handler(CommandHandler("startbirthday", birthday))
dp.add_handler(MessageHandler(Filters.text, sendSticker))


dp.add_error_handler(error)

updater.start_polling()

print("Your telegram bot is running!")

updater.idle()
