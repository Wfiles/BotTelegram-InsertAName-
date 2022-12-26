from urllib.request import urlopen

import json
import variables
import re
import random
import os

import datetime
import pytz

#imprt recommendation chat id
rec_chat_id = os.getenv('RECOMMENDATION_CHAT_ID')

#import stickers from json
with open("source/sticker_file.json", "r") as f:
    stickers = json.load(f)
f.close()

with open("source/birthdays.json", "r") as f:
    birthdays = json.load(f)
f.close()

#start the bot
def start(update, context):
    update.message.reply_text("wesh wesh canne à pêche")

#sends a poll to see who is on campus and where
def epfl(update, context):
    number = random.randint(1, 100)
    if number == 5:
        rickrolled(update, context)
        return

    chatID = update.message.chat.id
    variables.bot.send_poll(
        chat_id = chatID,
        question="where you at?",
        options = ["bc", "bibli inm", "inf", "rolex", "co", "cm", "migros", 
            "somewhere else sur campus", "somewhere else pas sur campus", "omw to campus"], 
        is_anonymous = False)

#sends the saisine audio
def storm(update, context):
    number = random.randint(1, 100)
    if number == 5:
        rickrolled(update, context)
        return

    chatID = update.message.chat.id
    with open("media/saisine.mp3", "rb") as f:
        update.message.reply_audio(audio=f)

    if update.message.from_user.username == "Jadel15":
        variables.bot.send_message(chat_id = chatID, text = "YOU ARE APPROACHING !")
    else:
        variables.bot.send_message(chat_id = chatID, text = "JAD IS APPROACHING !")

#sends stickers according to trigger words
def sendSticker(update, context):
    number = random.randint(1, 100)
    if number == 5:
        rickrolled(update, context)
        return

    chatID = update.message.chat.id
    #the stickers are send if the trigger word is contained in the message
    for sticker in stickers["teffe7aPackNotRestricted"]:
        for i in sticker['trigger words']:
            if i in update.message.text.lower():
                variables.bot.sendSticker(
                    chat_id = chatID, 
                    sticker = sticker['ref'])
                return

    #the stickers are sent if the trigger word is exclusively in the message
    for sticker in stickers["teffe7aPackRestricted"]:
        for i in sticker['trigger words']:
            if i == update.message.text.lower():
                variables.bot.sendSticker(
                    chat_id = chatID, 
                    sticker = sticker['ref'])
                return  

def recommendations(update, context):
    number = random.randint(1, 100)
    if number == 5:
        rickrolled(update, context)
        return

    initialmessage = update.message.text
    finalmessage = re.sub("/rec", "", initialmessage, count = 1)
    if finalmessage != "":
        user = update.message.from_user.username
        variables.bot.send_message(
            chat_id = rec_chat_id,
            text = f'{user} has sent this recommendation :{finalmessage}')

def rickrolled(update, context):
    with open("media/RickRolled.mp4", "rb") as f:
        update.message.reply_video(video=f)

def ban(update, context):
    text_reply = update.message.reply_to_message
    if text_reply is None:
        update.message.reply_text('On va te ban à toi')
        return

    user_sender =  update.message.reply_to_message.from_user.first_name
    chat_id = update.message.chat.id
    variables.bot.send_message(
        chat_id = chat_id,
        text = f'{user_sender} on te ban !'
    )

def birthday(update, context):
    time = datetime.now(pytz.timezone('Europe/Zurich'))
    if time().hour == 21 and time().minute == 10:
        for bday in birthdays:
            if time.day == bday['day'] and time.month == bday['month']:
                age = time.year - bday['year']
                if (bday['year'] == 2002):
                    variables.bot.send_message(
                        chat_id = rec_chat_id,
                        text = f'Happy birthday {bday["name"]} ! ur old, {age} ans déjà :| jk jk we love you anyway ;)')
                else:
                    variables.bot.send_message(
                        chat_id = rec_chat_id,
                        text = f'Happy birthday {bday["name"]} ! {age} ans déjà !!! we love you enjoy it au max ;)')

def kat(update, context):
    meow = "meow ^^"
    if random.randint(1, 10) > 5:
        folder = "media/kats"
        filename = os.path.join(folder, random.choice(os.listdir(folder)))
        with open(filename, "rb") as f:
            update.message.reply_photo(photo=f, caption=meow)
    else:
        url = "https://api.thecatapi.com/v1/images/search"
        response = urlopen(url)
        data_json = json.loads(response.read())
        update.message.reply_photo(photo=data_json[0]["url"], caption=meow)

def doggo(update, context):
    woof = "woof ^^"
    if random.randint(1, 10) > 5:
        folder = "media/doggos"
        filename = os.path.join(folder, random.choice(os.listdir(folder)))
        with open(filename, "rb") as f:
            update.message.reply_photo(photo=f, caption=woof)
    else:
        url = "https://api.thedogapi.com/v1/images/search"
        response = urlopen(url)
        data_json = json.loads(response.read())
        update.message.reply_photo(photo=data_json[0]["url"], caption=woof)

def memes(update, context):
    woof = "hehehe"
    if random.randint(1, 10) < 1:
        folder = "media/memes"
        filename = os.path.join(folder, random.choice(os.listdir(folder)))
        with open(filename, "rb") as f:
            update.message.reply_photo(photo=f, caption=woof)
    else:
        url = "https://api.imgflip.com/get_memes"
        response = urlopen(url)
        data_json = json.loads(response.read())
        update.message.reply_photo(photo=data_json[0]["url"], caption=woof)

def babypic(update, context):
    caption = "baby ^^"
    folder = "media/babypics"
    filename = os.path.join(folder, random.choice(os.listdir(folder)))
    with open(filename, "rb") as f:
        update.message.reply_photo(photo=f, caption=caption)