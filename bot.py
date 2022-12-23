import logging
import json
from subprocess import CalledProcessError
import requests
import random
import os
import re
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

PORT = int(os.environ.get('PORT', 5000))
TOKEN = os.getenv('API_TOKEN')

# Enable logging
logging.basicConfig(format = "%(asctime)s - %(name)s - %(levelname)s  - %(message)s", level = logging.INFO)

logger = logging.getLogger(__name__)

#if it is in chaotic mood it will not help when you want it to help (+ d'autres fonctionnalités si vous avez de l'inspi)
chaoticMood = True

#start the bot
def start(update, context):
    update.message.reply_text("wesh wesh canne à pêche")

#help function of the bot
def help(update, context):
    if chaoticMood :
        update.message.reply_text(
            """che7 je vais pas t'aider""")
    else :
        update.message.reply_text(
            """ok fine >:(
                /start : starts me,
                /help : gives you tmi about me
                /cat : sends cute cat pictures :3
                /epfl : creates a poll to see who is where (fkrk)
                ..."""
        )

#sends a poll to see who is on campus and where
#def epfl(update, context):
    ##help

#error function of the bot
def error(update, context):
    logger.info("i hate u you broke me :|, fix it: {context.error}")

#sends the saisine audio
def storm(self, update, context):
    print("bbbbbbbbbb")
    with open("media/saisine.mp3", "rb") as f:
        print("aaaaaaaaaa")
        update.message.reply_audio(audio=f)

    self.logger.info("JAD IS APPROACHING !")

#detects trigger words
def regexFilter(main, *keywords) : 
    filters = Filters.regex(re.compile(main, re.IGNORECASE))
    for k in keywords :
        filters |= Filters.regex(re.compile(k, re.IGNORECASE))
    return filters

#sends the react sticker
def reactSticker(sticker):
  return lambda update, context : update.message.reply_sticker(sticker, quote=False)

#associates trigger words to stickers
def addStickerUnrestricted(reaction, list):
    for i in list:
        dp.add_handler(MessageHandler(regexFilter(i), reactSticker(reaction)))

#def sendStickerRestricted(reaction, list):
#    for i in list:
#        dp.send_message(MessageHandler(regexFilter(i), reactSticker(reaction)))

#def modifyMood(*keywords):
#    if chaoticMood:
#        chaoticMood = False

##MAIN##
def main():
    updater = Updater(token = TOKEN, use_context = True)

    global dp
    dp = updater.dispatcher

    #add the function handlers for each function of the bot
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("storm", storm))
    #dp.add_handler(CommandHandler("epfl", epfl))

    with open("source/sticker_file.json", "r") as f:
        stickers = json.load(f)

    for sticker in stickers["teffe7aPackNotRestricted"]:
        addStickerUnrestricted(sticker['ref'], sticker['trigger words'])

    f.close()

    dp.add_error_handler(error)

    updater.start_polling()

    print("Your telegram bot is running!")

    updater.idle()

    #while updater.is_idle:
    #    for sticker in stickers["teffe7aPackRestricted"]:
    #        sendStickerRestricted(sticker['ref'], sticker['trigger words'])

if __name__ == '__main__': 
  main()