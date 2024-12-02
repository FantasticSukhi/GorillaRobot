class Config(object):
    LOGGER = True

    # Get this value from my.telegram.org/apps
    API_ID = 20353207
    API_HASH = "e5b2ac2f9c37bda345fa9fb5ade66961"

    CASH_API_KEY = "2ATSJ753CLE402MQ"  # Get this value for currency converter from https://www.alphavantage.co/support/#api-key

    DATABASE_URL = "postgres://mcclbjwx:CqMrbec47cqL5KbaZOUDlVQWOscjNcKR@peanut.db.elephantsql.com/mcclbjwx"  # A sql database url from elephantsql.com

    EVENT_LOGS = (-1002138809373)  # Event logs channel to note down important bot level events

    MONGO_DB_URI = "mongodb+srv://danishzain1637:papaspartan@cluster0.xdje3.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"  # Get ths value from cloud.mongodb.com

    # Telegraph link of the image which will be shown at start command.
    START_IMG = "http://ibb.co/j5XhNcZ"

    SUPPORT_CHAT = "MBV_CHATS"  # Your Telegram support group chat username where your users will go and bother you

    TOKEN = "6821828314:AAE--Dov6bT8xLs6AS3eWWKWkb6rQOlPHqs"  # Get bot token from @BotFather on Telegram

    TIME_API_KEY = "9LMMJQ30GM49"  # Get this value from https://timezonedb.com/api

    OWNER_ID = 6713994904  # User id of your telegram account (Must be integer)

    # Optional fields
    BL_CHATS = []  # List of groups that you want blacklisted.
    DRAGONS = []  # User id of sudo users
    DEV_USERS = []  # User id of dev users
    DEMONS = []  # User id of support users
    TIGERS = []  # User id of tiger users
    WOLVES = []  # User id of whitelist users

    ALLOW_CHATS = True
    ALLOW_EXCL = True
    DEL_CMDS = True
    INFOPIC = True
    LOAD = []
    NO_LOAD = []
    STRICT_GBAN = True
    TEMP_DOWNLOAD_DIRECTORY = "./"
    WORKERS = 8


class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
