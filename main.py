from dotenv import load_dotenv
from bot.bot import create_bot, register_handlers, run


load_dotenv()

if __name__ == "__main__":
    bot = create_bot()
    register_handlers(bot)
    run(bot)
