import variables
import random
import json

#import stickers from json
with open("source/sticker_file.json", "r") as f:
    stickers = json.load(f)
f.close()

def rickrolled(update, context):
    with open("media/RickRolled.mp4", "rb") as f:
        update.message.reply_video(video=f)
    f.close()

def ban(update, context):
    number = random.randint(1, 100)
    if number == 5:
        rickrolled(update, context)
        return
    
    text_reply = update.message.reply_to_message
    user = update.message.from_user.first_name
    user_sender =  update.message.reply_to_message.from_user.first_name
    chat_id = update.message.chat.id

    if text_reply is None:
        update.message.reply_text('On va te ban à toi')
        return
    
    if user_sender == "KachowBot":
        variables.bot.send_message(
        chat_id = chat_id,
        text = f'{user} pk tu me ban ? :( '
        ) 
        return
    variables.bot.send_message(
        chat_id = chat_id,
        text = f'{user_sender} on te ban !'
    )

#sends stickers according to trigger words
def sendSticker(update, context):
    number = random.randint(1, 500)
    if number != 5:
        return

    number = random.randint(1, 100)
    if number == 5:
        rickrolled(update, context)
        return

    chatID = update.message.chat.id
    #the stickers are send if the trigger word is contained in the message
    for sticker in stickers["teffe7aPackNotRestricted"]:
        for i in sticker['trigger words']:
            if i in update.message.text.lower():
                if sendStickerHelper(sticker, chatID):
                    return

    #the stickers are sent if the trigger word is exclusively in the message
    for sticker in stickers["teffe7aPackRestricted"]:
        for i in sticker['trigger words']:
            if i == update.message.text.lower():
                if sendStickerHelper(sticker, chatID):
                    return


def sendStickerHelper(sticker, chatID):
    if sticker['name'] == "feur":
        if random.randint(1, 2) == 1:
            variables.bot.sendSticker(
                chat_id = chatID, 
                sticker = sticker['ref'])
            return True
    else:
        variables.bot.sendSticker(
                    chat_id = chatID, 
                    sticker = sticker['ref'])
        return True