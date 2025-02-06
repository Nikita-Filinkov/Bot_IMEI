from decouple import config
import telebot

TOKEN_TELEGRAM = config('TOKEN_TELEGRAM')


class TelegramBot:
