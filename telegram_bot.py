"""
This telegram bot is created according to this tutorial: https://www.youtube.com/watch?v=NwBWW8cNCP4
with some variations though
"""


from lib_search_sdk import load_db, add_to_db, get_suggestions
from decouple import config
import telebot

API_KEY = config('API_KEY')

bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=['test'])
def echo_test(message):
    bot.reply_to(message, "I'm up and running")


@bot.message_handler(commands=['help', "start"])
def help_display(message):
    bot.reply_to(message, "\n \
    Welcome to the trie search bot. Here you can search through the example token list by typing in a prefix.\n \
    Try any prefix you like, just remember, that the database contains only lower-case latin letters.\n \
    By default this bot will return you maximum 10 suitable tokens.\n \
    To set maximum number of tokens to be returned, use /limit X command, where X is a positive integer.\n \
    If you type None instead of, the bot will try its best to return you all suitable tokens. \
    To see the current limit setting, use /limit command with no X argument")


my_db = load_db('tests/2466_tokens.txt')

limit = 10


@bot.message_handler(commands=['limit', 'limit=', 'lim'])
def set_limit(message):
    global limit
    lim_req = message.text.split()

    if len(lim_req) == 1:
        bot.reply_to(message, f"Currently limit is {limit}")
    elif len(lim_req) == 2:
        lim_value = lim_req[1]
        if lim_value == 'None':
            limit = None
            bot.reply_to(message, "No more limits any more: we'll try to return you all suitable tokens")
        elif lim_value.isdigit():
            limit = int(lim_value)
            bot.reply_to(message, f"Limit is set to {limit}")
        else:
            bot.reply_to(message, "To set the limit please type /limit X, where X is and integer number or None")
    else:
        bot.reply_to(message, "To set the limit please type /limit X, where X is and integer number or None")



@bot.message_handler(func=lambda m: True)
def get_suggs(message):
    req = message.text
    suggestions = get_suggestions(my_db, req, limit)
    suggs = '\n'.join(suggestions)
    bot.reply_to(message, suggs)

bot.remove_webhook()
bot.polling()

