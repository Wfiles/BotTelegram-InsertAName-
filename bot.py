import logging
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

#set of the stickers that the bot will send when trigger words are sent
teffe7aPack = {
    "scary jad"             : "CAACAgQAAxkBAAEGq8dji8npHraSlcWGyI8HYO45uarHFwACVg4AAi-xQVNVw2ytAUVEFCsE",
    "yassine masterclasse"  : "CAACAgQAAxkBAAEGq8lji8oD6HJFQV9zQXXSJa_slTjXuwACaQ0AAvY7QFObyhQn_yiQISsE", 
    "jad w/ knife"          : "CAACAgQAAxkBAAEGq8tji8oTkU42b-7T-ZGF2Qw2fQh5VAACvQ0AAiIFQVNpBT5dvS2hRSsE", 
    "mamoun"                : "CAACAgQAAxkBAAEGq81ji8ou-1UIYg8kR01x9JefhAABslUAAi0NAAK0VUlTwqD-X9j_maIrBA", 
    "L"                     : "CAACAgQAAxkBAAEGq89ji8o58Xa-BTMVT_wEIW6nUuGCMgACsA0AAkrKQVNfbuoOw8OncCsE", 
    "matthias wyss"         : "CAACAgQAAxkBAAEGq9Fji8pHxoVlf13YTYdevqucJAWz5gACYw0AAlLlQFOJMj8mM_ou-ysE", 
    "scary jad 2"           : "CAACAgQAAxkBAAEGq9Nji8pU_b6o0CKvvo2V_HReR0NOVQACFwwAApqxQVMcYL8vEYh0kCsE", 
    "greenscreen jad"       : "CAACAgQAAxkBAAEGq9Vji8pel4E1DqWR5VRS5XD5u0CPuwACQBAAAtNFSFOstDSZqAm61isE", 
    "pikachu mamoun"        : "CAACAgQAAxkBAAEGq9tji8px3AkDY8rX39EteoOVSf14kQACPQwAAkJgQVOMgGg6P46SfysE", 
    "unlike"                : "CAACAgQAAxkBAAEGq91ji8qLIZYWjSTwmVFKl77iEKPmWgACzA0AAvwAAUBT6qL7ZbjmkAUrBA", 
    "baguette"              : "CAACAgQAAxkBAAEGq99ji8qVsDTvqoUuWyB8YFudMjOwAAMZDAAC4rtJU8ktQZImeNcRKwQ", 
    "dalle"                 : "CAACAgQAAxkBAAEGq9lji8pp02JHGbRciVnQQg8xcOGATgAC9A0AAmvkQVOG-A9OTdcptysE", 
    "urs knife 1"           : "CAACAgQAAxkBAAEGq-Fji8qlFFasUn0qLzmzJKxRZ6QryQACdQ4AAl0RQFM5ayBNlMZnhSsE",
    "urs knife 2"           : "CAACAgQAAxkBAAEGq-Nji8qybAFE6RnYJuEL9Tj41VaduAACrgsAAlE5QVPsZRcr5-GmzSsE",
    "urs knife 3"           : "CAACAgQAAxkBAAEGq-dji8rTp3b1y2Nvcimkpr4DqHxFHQACrQ0AAifAQFP9uZmDXSrObSsE",
    "urs knife 4"           : "CAACAgQAAxkBAAEGq-Vji8rClT1g4CsITDSnyP_i6xIpDwACdw0AAlZoQVPa3t6w_kuH1SsE",
    "urs knife 5"           : "CAACAgQAAxkBAAEGq-lji8rgtczeJb4eboSq99zCTpZCcgACIQ0AAuGUQFNPYoJb2dVADSsE",
    "emergency exit"        : "CAACAgQAAxkBAAEGq-tji8rrqt_y4OG3KbCHTbdMOwLRBwAC6Q0AAjr8QVOBAj8v1tVpiCsE", 
    "agepAuLit"             : "CAACAgQAAxkBAAEGq-1ji8r3W-UDDa-5XspPsjpHZD3VxgACGA8AAihAIFDiSO3j6T5JuCsE", 
    "basé"                  : "CAACAgQAAxkBAAEGq_Jji8sDUguYvgi-lpUewGkeKyFjEQAChA0AAncEUFPS0h_m7nbUnysE",
    "cap"                   : "CAACAgQAAxkBAAEGq_Zji8sO51887Uw-KHmudoz8458kGAACKgwAAtG3SVN0Qv2iJ939hSsE",
    "réel"                  : "CAACAgQAAxkBAAEGq_hji8sZTDf2HPX_cAqZuvOvRsOuUgAC4AwAAoHySVOx8Q51K2QsRysE",
    "crowd"                 : "CAACAgQAAxkBAAEGq_pji8spBGsk4OysbOpcOyvSV3tyyQACfwwAAoClSFNdCigDThtScisE",
    "bagarre"               : "CAACAgQAAxkBAAEGq_xji8tDgHRA2RALK1tZvgAB2iBuLIUAAvkOAAJs2UFTNteSUzyooJ8rBA", 
    "wasted"                : "CAACAgQAAxkBAAEGrAJji8tmNlULam_vDGaz9GzpsO28VgACvQ0AAsEYSVMAAYUFRS6YWiQrBA",
    "à fond"                : "CAACAgQAAxkBAAEGrAABY4vLUgABIWiXnT_7yP_pcC4PY_zzAAL4DgAC4OdQU_0ccNq9jgX0KwQ", 
    "algebre"               : "CAACAgQAAxkBAAEGrARji8t3Ff3xaqx4orIN_P8bxS2y0QAC8QwAAquZSVN9I3O3nPxZOCsE",
    "sunglasses omar"       : "CAACAgQAAxkBAAEGrARji8t3Ff3xaqx4orIN_P8bxS2y0QAC8QwAAquZSVN9I3O3nPxZOCsE",
    "colonel"               : "CAACAgQAAxkBAAEGrAhji8uXgyrXShqwT9zABDPGlq037AACtQsAAqbFUVNVEDfLffQv3isE",
    "dinguerie wesh"        : "CAACAgQAAxkBAAEGrApji8uoDegAAd_nueXS3gJnL88pMpsAArkNAAIyTklTNwXLaNPZdB0rBA",
    "hassen thinking"       : "CAACAgQAAxkBAAEGrAxji8u4LjToA25jvoC-u9z4sycUGQACDwoAArVoSVNCibIFymEVFCsE",
    "sofia imposteur"       : "CAACAgQAAxkBAAEGrA5ji8vHWHiUnWkhDAUYwa0ux2zrIgACCQ0AAv-XSVP4BLATBaDSgysE",
    "imagine"               : "CAACAgQAAxkBAAEGrBBji8vXyAE6yoJAV3CkoAU6FqU3mQAC3Q4AAqscUFPtTOSO6791BCsE",
    "caddie"                : "CAACAgQAAxkBAAEGrBJji8vmG39MjCwcpbNSbDyCaqpklQACyA4AAjNBUFOCK08NznTGtysE",
    "jad filou"             : "CAACAgQAAxkBAAEGrBRji8v8yzp7qIkGv4nhPqj42TLIhgACaA0AAh5fcVM8GPwnmvIcnysE",
    "IC Wars"               : "CAACAgQAAxkBAAEGrBZji8xb-DI4MjiQKYnhIwFVrTLddwACqg8AAs8saFM4O9CITuSxiSsE",
    "yass queen"            : "CAACAgQAAxkBAAEGrBhji8xuNrGY1_3-T1lCkyDV13HDsAACLhAAAv5QaVOn7zzRubnoPCsE",
    "wiwi filou"            : "CAACAgQAAxkBAAEGrBpji8yBbSLVVh13ptefzclLEihf_wAC5xAAAgXjgFMj5eQzTpdBYisE",
    "fax"                   : "CAACAgQAAxkBAAEGrBxji8yYptZKdNAQMy9ogRldpe16uwACuA8AAuCfiFNgrFXK2HJj-SsE",
    "yas strong"            : "CAACAgQAAxkBAAEGrB5ji8yp_VGgQbIlkoR9SdNSQLUlBQACfAsAAsSukVOUL-KAz5cn6isE",
    "aveugle"               : "CAACAgQAAxkBAAEGrCJji80Z-zcQOdw4XTKWAntGOpZ8zAACrA4AApd6qVM7HkoJ1G45ZisE",
    "rien à foutre"         : "CAACAgQAAxkBAAEGrCRji80oa0bNh98HHSN-lVl7F2MHhAACLgwAAkB8sVOf0ZHTW0hYnCsE",
    "kratos messi"          : "CAACAgQAAxkBAAEGrCZji803Wn9VWkOBbVBGgj-c0CiPXwACtQ4AAk9VGVAwKG_C9epUWCsE",
    "sorcellerie"           : "CAACAgQAAxkBAAEGrChji81LnGyfbrZBRe6z_vqtMnVlswACHw0AAgiRIFCUZ2ukf8yNsysE",
    "coolos"                : "CAACAgQAAxkBAAEGrftjjMVvwD4kSw-6o0QbzrI5JWS2EAACZg4AAlDwYVC5MaFFqV88visE",
    "help needed"           : "CAACAgQAAxkBAAEG4PJjnyS79UnudFlx9dVVpsCB9xdkNgACVQ0AAnihcVDCmb4Iae1SYywE",
    "lina zinzin"           : "CAACAgQAAxkBAAEG4PZjnyTmVrEbYltpBZf0MRWbtsWeLQACHxcAAlv9eVAflkpCbug88SwE",
    "chillax"               : "CAACAgQAAxkBAAEG4P1jnyU3AAGgxUShHt_RYU-IaocCkqUAAjsQAAIdCJlQFETJfZI-jIAsBA",
    "hater"                 : "CAACAgQAAxkBAAEG4QABY58lThn5lsd4vRAgKoFePpdqCQUAApARAAKSTcBQrr_hhJrN9DEsBA",
    "ratio"                 : "CAACAgQAAxkBAAEG4QJjnyViwQGbMQw4zxZUVyIu18TZIAAC-gsAAlev2FD73V4FnwSUyCwE",
    "smh"                   : "CAACAgQAAxkBAAEG4QRjnyV0sICZ9s4YtOQeKW2hF2j9fwACmxAAAqOz2FAFJ7kksH6NXiwE",
    "mérité"                : "CAACAgQAAxkBAAEG4QhjnyWRMddP5sHyUTb3G75wZLgm4AACFBAAAkoz2FAECxLj7CnPMywE",
    "hapi"                  : "CAACAgQAAxkBAAEG4QpjnyWjXPPZZd0kbzYHtWzOSC9ELQAC1Q8AAmtY0VC0YL3qAfi7ViwE",
    "noel"                  : "CAACAgQAAxkBAAEG4QxjnyW1yqnVQSyiayls07pJB--vDAACBhIAAm672VAQII2aIu1NbiwE",
    "feur"                  : "CAACAgQAAxkBAAEG4Q5jnyXEFiUdBclzT_aKT9nK1_1vUQACvw0AAuFj4VBM460n4dzeXCwE",
    "unlucky"               : "CAACAgQAAxkBAAEG4RJjnyXV6oFUZHtweGhaMM0kytdPqwACTA4AAnz24FC9GiXKtYi3PywE",
    "sayé"                  : "CAACAgQAAxkBAAEG4RpjnyXkAR9aaXbDdzjN12AW6Qj1NwACig8AAl3i4VBYzR7A7IaS0iwE"
}

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
def addSticker(reaction, *keywords):
    dp.add_handler(MessageHandler(regexFilter(*keywords), reactSticker(reaction)))

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
    #dp.add_handler(CommandHandler("epfl", epfl))

    #link trigger words to stickers
    addSticker(teffe7aPack["scary jad"]             , "come")
    addSticker(teffe7aPack["yassine masterclasse"]  , "masterclasse", "pres", "vp", "il faut donner crédit là où crédit est dû")
    #addSticker(teffe7aPack["jad w/ knife"]          , )
    addSticker(teffe7aPack["mamoun"]                , "desert", "maroc")
    addSticker(teffe7aPack["L"]                     , "cheh", "che7") #to add L et F
    addSticker(teffe7aPack["matthias wyss"]         , "LeBron James")
    #addSticker(teffe7aPack["scary jad 2"]           , )
    addSticker(teffe7aPack["greenscreen jad"]       , "no way")
    #addSticker(teffe7aPack["pikachu mamoun"]        , )
    addSticker(teffe7aPack["unlike"]                , "nul")
    addSticker(teffe7aPack["baguette"]              , "baguette", "pain")
    addSticker(teffe7aPack["dalle"]                 , "j'ai faim", "dalle", "on mange quoi")
    #addSticker(teffe7aPack["urs knife 1"]           , )
    #addSticker(teffe7aPack["urs knife 2"]           , )
    #addSticker(teffe7aPack["urs knife 3"]           , )
    #addSticker(teffe7aPack["urs knife 4"]           , )
    #addSticker(teffe7aPack["urs knife 5"]           , )
    addSticker(teffe7aPack["emergency exit"]        , "head out", "emergency")
    addSticker(teffe7aPack["agepAuLit"]             , "rompichâmes", "bonne nuit", "rompichames")
    addSticker(teffe7aPack["basé"]                  , "basé", "base", "based")
    addSticker(teffe7aPack["cap"]                   , "cap", "tu mens", "menteur", "menteuse")
    addSticker(teffe7aPack["réel"]                  , "réel", "reel", "real")
    #addSticker(teffe7aPack["crowd"]                 , )
    addSticker(teffe7aPack["bagarre"]               , "bagarre", "combat", "battre", "bagarrer", "frapper", "tapper")
    addSticker(teffe7aPack["wasted"]                , "dead", "mort", "morte", "meurt")
    addSticker(teffe7aPack["à fond"]                , "à fond", "a fond")
    addSticker(teffe7aPack["algebre"]               , "algebre", "algèbre", "aadjad", "aanjad")
    addSticker(teffe7aPack["sunglasses omar"]       , "eywa")
    addSticker(teffe7aPack["colonel"]               , "colonel")
    addSticker(teffe7aPack["dinguerie wesh"]        , "dinguerie", "dinguerie wesh")
    addSticker(teffe7aPack["hassen thinking"]       , "hmmm", "hmm", "mmm", "mmmm", "hmmmmmmm")
    addSticker(teffe7aPack["sofia imposteur"]       , "imposteur", "impostor", "amogus", "sus")
    addSticker(teffe7aPack["imagine"]               , "imagine")
    #addSticker(teffe7aPack["caddie"]                , )
    addSticker(teffe7aPack["jad filou"]             , "filou")
    addSticker(teffe7aPack["IC Wars"]               , "i see")
    addSticker(teffe7aPack["yass queen"]            , "yass queen", "yassqueen", "yasqueen", "yas queen", "slay", "queen")
    addSticker(teffe7aPack["wiwi filou"]            , "ours")
    addSticker(teffe7aPack["fax"]                   , "facts", "fax")
    addSticker(teffe7aPack["yas strong"]            , "alpha", "beta", "omega", "sigma", "strong", "fort")
    #addSticker(teffe7aPack["aveugle"]               , )
    addSticker(teffe7aPack["rien à foutre"]         , "rien à foutre", "raf", "blc", "balec", "jmf", "menfou", "je m'enfout")
    addSticker(teffe7aPack["kratos messi"]          , "kratos", "messi")
    addSticker(teffe7aPack["sorcellerie"]           , "incroyable", "sorcellerie", "wtf")
    addSticker(teffe7aPack["coolos"]                , "drip", "coolos", "cool")
    addSticker(teffe7aPack["help needed"]           , "aled", "help")
    addSticker(teffe7aPack["lina zinzin"]           , "zinzin")
    addSticker(teffe7aPack["chillax"]               , "chillos")
    addSticker(teffe7aPack["hater"]                 , "hater")
    addSticker(teffe7aPack["ratio"]                 , "ratio")
    #addSticker(teffe7aPack["smh"]                   , )
    addSticker(teffe7aPack["mérité"]                , "mérité")
    addSticker(teffe7aPack["hapi"]                  , "happy", "content")
    addSticker(teffe7aPack["noel"]                  , "noel")
    addSticker(teffe7aPack["feur"]                  , "quoi")
    #addSticker(teffe7aPack["unlucky"]               , )
    addSticker(teffe7aPack["sayé"]                  , "sayé", "saye")

    dp.add_error_handler(error)

    updater.start_polling()

    print("Your telegram bot is running!")

    updater.idle()

if __name__ == '__main__': 
  main()