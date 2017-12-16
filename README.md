# CryptoCoinsInfoBot

[@CryptoCoinsInfoBot](https://t.me/CryptoCoinsInfoBot "@CryptoCoinsInfoBot") - enjoy it!

This is a simple version of a Telegram Bot, has been used [pyTelegramBotAPI Library ](https://github.com/eternnoir/pyTelegramBotAPI "pyTelegramBotAPI Library GitHub Repository") with using webhook updates method for recieve the messages.  

For use unicode emojis has been used [Emoji Library](https://github.com/carpedm20/emoji "Emoji for Python.")

---

Has been deployed on Heroku servers. Put the Token of you bot and the URL of your heroku app to the Heroku environment settings:

+ For setting up variables:
```bash
$ heroku config:set TOKEN=put_your_token_here
$ heroku config:set APPURL=put_your_app_url_here
$ heroku config:set YOURALIAS=put_your_telegram_alias
```

+ For show your configs vars:
```bash
$ heroku config
```