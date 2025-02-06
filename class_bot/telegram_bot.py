from decouple import config
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests

TOKEN_TELEGRAM = config('TOKEN_TELEGRAM')