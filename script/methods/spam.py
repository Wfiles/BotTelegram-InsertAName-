from urllib.request import urlopen

import variables
import json
import random
import os

from datetime import datetime
import pytz

from methods.troll import rickrolled

kachow_chat_id = os.getenv('KACHOW_CHAT_ID')

with open("source/compliments.json", "r") as f:
    compliments = json.load(f)
f.close()

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
    caption = "hehehe"
    #if random.randint(1, 10) < 1:
    folder = "media/memes"
    filename = os.path.join(folder, random.choice(os.listdir(folder)))
    with open(filename, "rb") as f:
        update.message.reply_photo(photo=f, caption=caption)
    #else:
    #    url = "https://api.imgflip.com/get_memes"
    #    response = urlopen(url)
    #    data_json = json.loads(response.read())
    #    update.message.reply_photo(photo=data_json[0]["url"], caption=woof)

def babypic(update, context):
    caption = "baby ^^"
    folder = "media/babypics"
    filename = os.path.join(folder, random.choice(os.listdir(folder)))
    with open(filename, "rb") as f:
        update.message.reply_photo(photo=f, caption=caption)

def complimentme(update, context):
    number = random.randint(1, 100)
    if number == 5:
        rickrolled(update, context)
        return
    index = random.randint(0, len(compliments["compliments"]))
    update.message.reply_text(compliments["compliments"][index])

def copains(update, context):
    caption = "hehe <3"
    folder = "media/copains"
    filename = os.path.join(folder, random.choice(os.listdir(folder)))
    with open(filename, "rb") as f:
        update.message.reply_photo(photo=f, caption=caption)

def aaa(update, context):
    user = update.message.from_user.first_name
    variables.bot.send_message(chat_id = update.message.chat.id, text = f'{user} wants to say : AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')

def birthday(update, context):
    time = datetime.now(pytz.timezone('Europe/Zurich'))
    job_queue = updater.job_queue
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
