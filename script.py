import telebot

bot = telebot.TeleBot("8333896356:AAERB58Gb6k6scltmwf25j053nShy49NySo")

bot.remove_webhook()
bot.set_webhook("https://functions.yandexcloud.net/d4eilkdcnq5n6inkdvl2")