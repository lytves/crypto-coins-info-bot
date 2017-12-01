import telebot
import os
import requests
from flask import Flask, request

# set up config variables en your heroku environment
# your bot TOKEN
token = os.environ.get('TOKEN')
# your heroku app URL and add path "bot" for active update
appURL = os.environ.get('APPURL') + '/bot'
# end of read config variables

bot = telebot.TeleBot(token)

server = Flask(__name__)

# on the start command to user would send a userkeyboard
@bot.message_handler(commands=['start'])
def start(message):
    # create userkeyboard, resize = true, autohide=true
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row("/Bitcoin", "/Ethereum")
    user_markup.row("/BitConnect", "/BitcoinCash")
    user_markup.row("/settings")

    # send a message to a user with new keyboard
    bot.send_message(message.from_user.id, 'Hello, ' + message.from_user.first_name
                     + '. I am your Crypto Coins Info Bot! Use a keyboard for receive info about a price of a crypto coin.',
                     reply_markup=user_markup)


################################################## commands for recieve info
### BTC
@bot.message_handler(commands=['Bitcoin'])
def bitcoin(message):
    # BTC currency
    text = requestAPI(message, "bitcoin")

### ETH
@bot.message_handler(commands=['Ethereum'])
def ethereum(message):
    # ETH currency
    text = requestAPI(message, "ethereum")

### BCC
@bot.message_handler(commands=['BitConnect'])
def bitconnect(message):
    # LTC currency
    text = requestAPI(message, "bitconnect")

### LTC
@bot.message_handler(commands=['BitcoinCash'])
def litecoin(message):
    # LTC currency
    text = requestAPI(message, "bitcoin-cash")
################################## end of block of commands for recieve info

################################################## settings
### BTC
@bot.message_handler(commands=['settings'])
def settings(message):
    # print("this url:" + url)
    print("this url:")
################################## end of settings  block

def requestAPI(message, coin):
    url = "https://api.coinmarketcap.com/v1/ticker/" + str(coin)
    print("this url:" + url)
    response = requests.get(url)
    name = response.json()[0]['name']
    price = response.json()[0]['price_usd']
    rate24h = response.json()[0]['percent_change_24h']
    rate7d = response.json()[0]['percent_change_7d']
    text = "Current *" + name + "* price - *${}".format(price) + "*" \
           + "\nLast 24 hours changed for: `" + rate24h + "%`" \
           + "\nLast 7 days changed for: `" + rate7d + "%`"
    bot.send_message(message.from_user.id, text, parse_mode="Markdown")

# for reply for user with its own message
# @bot.message_handler(func=lambda message: True, content_types=['text'])
#def echo_message(message):
#    bot.reply_to(message, message.text)
# end

@server.route("/bot", methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=appURL)
    return "!", 200


server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
server = Flask(__name__)