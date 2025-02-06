from api_handler.api_handler import IMEICheckBot
import telebot
from decouple import config

TOKEN = config('TOKEN_TELEGRAM')
WHITE_LIST = [1432279864, 111111111]

bot = telebot.TeleBot(TOKEN)
bot.delete_webhook()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    """
        Функция обработчик сообщений для команды /start.

        Args:
            message (telebot.types.Message): Сообщение пользователя.

    """
    bot.reply_to(message, "Привет! Отправь мне IMEI устройства")


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    """
        Функция обработчик сообщений для всех остальных сообщений.

        Args:
            message (telebot.types. Message): Сообщение пользователя.

    """
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
