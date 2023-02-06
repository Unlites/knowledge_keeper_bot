from bot.bot import bot
from logger.logger import log
from handlers.handlers import *


def run():
    log.info("Starting bot...")
    bot.infinity_polling()