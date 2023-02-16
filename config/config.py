from os import environ as env


class Config:
    BOT_TOKEN = env['BOT_TOKEN']
    REDIS_HOST=env['REDIS_HOST']
    REDIS_PORT=env['REDIS_PORT']
    REDIS_PASSWORD=env['REDIS_PASSWORD']
    API_URL=env['API_URL']
    SIGN_IN_URL=env['SIGN_IN_URL']
    SIGN_UP_URL=env['SIGN_UP_URL']