import logging
import variables
import os
import random
import telegram

from methods import start, storm, epfl, recommendations, sendSticker, rickrolled, ban, birthday, kat, doggo, memes, babypic
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

PORT = int(os.environ.get('PORT', 5000))
TOKEN = '5862212486:AAFZmdpodJByZPh6GJM5QdY4MLac6-9eePs' #os.getenv('API_TOKEN')

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
/kat : sends a cute car picture :3
/doggo : sends a cute dog picture :>
/babypic : self explanatory :D
/rec : sends us recommendations about what you want to see, you only need to send the message in the format '/rec blabla' :)
...""")

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
dp.add_handler(CommandHandler("meme", memes))
dp.add_handler(CommandHandler("babypic", babypic))
dp.add_handler(MessageHandler(Filters.text, sendSticker))

dp.add_error_handler(error)

updater.start_polling()

print("Your telegram bot is running!")

updater.idle()

#while True:
#    birthday()
