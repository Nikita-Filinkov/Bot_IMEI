from api_handler.api_handler import IMEICheckBot
import telebot
from decouple import config

TOKEN = config('TOKEN_TELEGRAM')
WHITE_LIST = [1432279864, 1432279864]

bot = telebot.TeleBot(TOKEN)
bot.delete_webhook()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Отправь мне IMEI устройства")


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    if message.from_user.id not in WHITE_LIST:
        return bot.send_message(message.chat.id, 'Вас нет в списке разрешённых пользователей')

    if message.text:
        imei = message.text
        if len(imei) != 15 or not imei.isdigit():
            bot.reply_to(message, "IMEI должен быть числовым кодом длиной 15 символов")
        else:
            imei_api = IMEICheckBot(imei)
            info = imei_api.info()
            bot.reply_to(message, info)


bot.polling()
