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
    user_markup.row("/bitcoin", "/ethereum")
    user_markup.row("/bitconnect", "/litecoin")
    user_markup.row("/settings")

    # send a message to a user with new keyboard
    bot.send_message(message.from_user.id, 'Hello, ' + message.from_user.first_name
                     + '. I am your Crypto Coins Info Bot! Use a keyboard for receive info about a price of a crypto coin.',
                     reply_markup=user_markup)


################################################## commands for recieve info
### BTC
@bot.message_handler(commands=['bitcoin'])
def bitcoin(message):
    # BTC currency
    text = requestAPI(message, "bitcoin")

### ETH
@bot.message_handler(commands=['ethereum'])
def ethereum(message):
    # ETH currency
    text = requestAPI(message, "ethereum")

### BCC
@bot.message_handler(commands=['bitconnect'])
def bitconnect(message):
    # LTC currency
    text = requestAPI(message, "bitconnect")

### LTC
@bot.message_handler(commands=['litecoin'])
def litecoin(message):
    # LTC currency
    text = requestAPI(message, "litecoin")

################################## end of block of commands for recieve info

def requestAPI(message, coin):
    url = "https://api.coinmarketcap.com/v1/ticker/" + str(coin)
    print("this url:" + url)
    response = requests.get(url)
    name = response.json()[0]['name']
    price = response.json()[0]['price_usd']
    rate24h = response.json()[0]['percent_change_24h']
    rate7d = response.json()[0]['percent_change_7d']
    text = "Current " + name + " price - ${}".format(price) \
           + "\nLast 24 hours changed for: " + rate24h + "%" \
           + "\nLast 7 days changed for: " + rate7d + "%"
    bot.send_message(message.from_user.id, text)

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