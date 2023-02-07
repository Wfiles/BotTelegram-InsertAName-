import json
import variables
import re
import os

import pytz

#import recommendation chat id
rec_chat_id = -826861106 #os.getenv('RECOMMENDATION_CHAT_ID')

with open("source/birthdays.json", "r") as f:
    birthdays = json.load(f)
f.close()

#start the bot
def start(update, context):
    update.message.reply_text("wesh wesh canne à pêche")

def recommendations(update, context):
    initialmessage = update.message.text
    finalmessage = re.sub("/rec", "", initialmessage, count = 1)
    if finalmessage != "":
        user = update.message.from_user.username
        variables.bot.send_message(
            chat_id = rec_chat_id,
            text = f'{user} has sent this recommendation :{finalmessage}')
