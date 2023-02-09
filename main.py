from dotenv import load_dotenv
from handlers.bot import bot

load_dotenv()

if __name__ == '__main__':
    bot.infinity_polling()