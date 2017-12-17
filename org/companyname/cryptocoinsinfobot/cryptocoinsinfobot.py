import telebot
import os
import requests
from flask import Flask, request
from org.companyname.cryptocoinsinfobot.requestAPI import requestAPI

# set up config variables en your heroku environment
# your bot TOKEN
token = os.environ.get('TOKEN')
# your heroku app URL and add path "bot" for active update
appURL = os.environ.get('APPURL') + '/bot'
yourAlias = os.environ.get('YOURALIAS')
# end of read config variables

bot = telebot.TeleBot(token)

server = Flask(__name__)

# create userkeyboard, resize = true, autohide=false
user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
user_markup.row("Bitcoin", "Ethereum")
user_markup.row("BitConnect", "BitcoinCash")
user_markup.row("Ripple", "➡ 2")

user_markup2 = telebot.types.ReplyKeyboardMarkup(True, False)
user_markup2.row("Litecoin", "Cardano")
user_markup2.row("IOTA", "Dash")
user_markup2.row("1 ⬅", "➡ 3")

user_markup3 = telebot.types.ReplyKeyboardMarkup(True, False)
user_markup3.row("NEM", "Monero")
user_markup3.row("NEO", "feedback")
user_markup3.row("2 ⬅", "settings")

# send a start message
@bot.message_handler(func=lambda message: message.text == 'start')
def start(message):
    bot.send_message(message.from_user.id, 'Hello, ' + message.from_user.first_name
                     + '. I am your Crypto Coins Info Bot! Use a keyboard for receive info about a price of a crypto coin.',
                     reply_markup=user_markup)


# more coins list
@bot.message_handler(func=lambda message: message.text == '➡ 3')
def other_coins(message):
    bot.send_message(message.from_user.id, 'page 3', reply_markup=user_markup3)


# more coins list
@bot.message_handler(func=lambda message: message.text == '➡ 2' or message.text == '2 ⬅')
def other_coins(message):
    bot.send_message(message.from_user.id, 'page 2', reply_markup=user_markup2)


# main coins list
@bot.message_handler(func=lambda message: message.text == '1 ⬅')
def more_coins(message):
    bot.send_message(message.from_user.id, 'page 1', reply_markup=user_markup)

# settings command handler
@bot.message_handler(func=lambda message: message.text == 'settings')
def settings(message):
    # send a message to a user with new keyboard
    bot.send_message(message.from_user.id, 'coming soon... maybe', reply_markup=user_markup3)


# feedback command handler
@bot.message_handler(func=lambda message: message.text == 'feedback')
def feedback(message):
    # send a message to a user with new keyboard
    bot.send_message(message.from_user.id, 'Send your opinion about the bot to ' + yourAlias + ', please',
                     reply_markup=user_markup3)


################################################## handlers for the coins text name
### BTC
@bot.message_handler(func=lambda message: message.text == 'Bitcoin')
def bitcoin(message):
    text = requestAPI(message, "bitcoin", user_markup, bot)


### ETH
@bot.message_handler(func=lambda message: message.text == 'Ethereum')
def ethereum(message):
    text = requestAPI(message, "ethereum", user_markup, bot)


### BCC
@bot.message_handler(func=lambda message: message.text == 'BitConnect')
def bitconnect(message):
    text = requestAPI(message, "bitconnect", user_markup, bot)

### BCH
@bot.message_handler(func=lambda message: message.text == 'BitcoinCash')
def bitcoincash(message):
    text = requestAPI(message, "bitcoin-cash", user_markup, bot)


### XRP
@bot.message_handler(func=lambda message: message.text == 'Ripple')
def ripple(message):
    text = requestAPI(message, "ripple", user_markup, bot)


### LTC
@bot.message_handler(func=lambda message: message.text == 'Litecoin')
def litecoin(message):
    text = requestAPI(message, "litecoin", user_markup2, bot)


### ADA
@bot.message_handler(func=lambda message: message.text == 'Cardano')
def cardano(message):
    text = requestAPI(message, "cardano", user_markup2, bot)


### MIOTA
@bot.message_handler(func=lambda message: message.text == 'IOTA')
def iota(message):
    text = requestAPI(message, "iota", user_markup2, bot)


### Dash
@bot.message_handler(func=lambda message: message.text == 'Dash')
def dash(message):
    text = requestAPI(message, "dash", user_markup2, bot)


### NEM
@bot.message_handler(func=lambda message: message.text == 'NEM')
def nem(message):
    text = requestAPI(message, "nem", user_markup3, bot)


### Monero
@bot.message_handler(func=lambda message: message.text == 'Monero')
def monero(message):
    text = requestAPI(message, "monero", user_markup3, bot)


### NEO
@bot.message_handler(func=lambda message: message.text == 'NEO')
def neo(message):
    text = requestAPI(message, "neo", user_markup3, bot)
################################## end of handlers for the coins text name


### text messages handler for send user keyboard for all users
@bot.message_handler(func=lambda message: True)
def settings(message):
    bot.send_message(message.from_user.id, 'Hello, ' + message.from_user.first_name + '.', reply_markup=user_markup)
################################## end of settings  block


@server.route("/bot", methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=appURL)
    return "!", 200


server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
server = Flask(__name__)