import variables
import random

from methods.troll import rickrolled

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

def onmangeou(update, context):
    number = random.randint(1, 100)
    if number == 5:
        rickrolled(update, context)
        return

    chatID = update.message.chat.id
    variables.bot.send_poll(
        chat_id = chatID,
        question="manger ?",
        options = ["bc", "piano", "migros", "roulottes", "food lab", "espla", "migros", 
            "ornithorynque", "somewhere else sur campus", "somewhere else pas sur campus"], 
        is_anonymous = False)