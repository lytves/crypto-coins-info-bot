import requests
from emoji import emojize


def requestAPI(message, coin, user_markup, bot):
    url = "https://api.coinmarketcap.com/v1/ticker/" + str(coin)
    response = requests.get(url)
    name = response.json()[0]['name']
    price = response.json()[0]['price_usd']

    # 24 hours price change with emoji
    rate24h = response.json()[0]['percent_change_24h']
    if float(rate24h) > 20.0:
        rate24hemoji = emojize(":rocket:", use_aliases=True)
    elif float(rate24h) <= -20.0:
        rate24hemoji = emojize(":sos:", use_aliases=True)
    elif float(rate24h) < 0.0:
        rate24hemoji = emojize(":small_red_triangle_down:", use_aliases=True)
    elif float(rate24h) > 0.0:
        rate24hemoji = emojize(":white_check_mark:", use_aliases=True)

    # 7 days price change with emoji
    rate7d = response.json()[0]['percent_change_7d']
    if float(rate7d) > 20.0:
        rate7demoji = emojize(":rocket:", use_aliases=True)
    elif float(rate7d) <= -20.0:
        rate7demoji = emojize(":sos:", use_aliases=True)
    elif float(rate7d) < 0.0:
        rate7demoji = emojize(":small_red_triangle_down:", use_aliases=True)
    elif float(rate7d) > 0.0:
        rate7demoji = emojize(":white_check_mark:", use_aliases=True)

    text = "Current *" + name + "* price - *${}".format(price) + "*" \
           + "\nLast 24hours changed for *" + rate24h + "%*" + rate24hemoji \
           + "\nLast 7days changed for *" + rate7d + "%*" + rate7demoji

    bot.send_message(message.from_user.id, text, parse_mode="Markdown", reply_markup=user_markup)