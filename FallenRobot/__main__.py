import importlib
import re
import time
from platform import python_version as y
from sys import argv

from pyrogram import __version__ as pyrover
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram import __version__ as telever
from telegram.error import (
    BadRequest,
    ChatMigrated,
    NetworkError,
    TelegramError,
    TimedOut,
    Unauthorized,
)
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
)
from telegram.ext.dispatcher import DispatcherHandlerStop, run_async
from telegram.utils.helpers import escape_markdown
from telethon import __version__ as tlhver

import FallenRobot.modules.sql.users_sql as sql
from FallenRobot import (
    BOT_NAME,
    BOT_USERNAME,
    LOGGER,
    OWNER_ID,
    START_IMG,
    SUPPORT_CHAT,
    TOKEN,
    StartTime,
    dispatcher,
    pbot,
    telethn,
    updater,
)
from FallenRobot.modules import ALL_MODULES
from FallenRobot.modules.helper_funcs.chat_status import is_user_admin
from FallenRobot.modules.helper_funcs.misc import paginate_modules


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


PM_START_TEXT = """
*𝐇𝐞𝐥𝐥𝐨 𝐁𝐢𝐫𝐨* {}, 🥀

*๏ 🅘 🅐🅜* {} !
⩺ 𝕴 𝖆𝖒 𝖙𝖍𝖊 𝖘𝖕𝖊𝖈𝖎𝖆𝖑 𝖌𝖗𝖔𝖚𝖕 𝖒𝖆𝖓𝖆𝖌𝖊𝖒𝖊𝖓𝖙 𝖇𝖔𝖙 𝖜𝖎𝖙𝖍 𝖓𝖊𝖜 𝖆𝖓𝖉 𝖘𝖕𝖊𝖈𝖎𝖆𝖑 𝖋𝖊𝖆𝖙𝖚𝖗𝖊𝖘. 𝕳𝖊𝖞𝖆𝖆 𝕭𝖎𝖗𝖔 !!!!! 𝕴 𝖐𝖓𝖔𝖜 𝖞𝖔𝖚 𝖆𝖗𝖊 𝖕𝖎𝖗𝖔.
   𝔉𝔢𝔞𝔱𝔲𝔯𝔢𝔰 :-
1️⃣<<<==>>> 𝔅𝔞𝔫 𝔓𝔬𝔴𝔢𝔯
2️⃣<<<==>>> 𝔊𝔟𝔞𝔫 𝔓𝔬𝔴𝔢𝔯
3️⃣<<<==>>> ℭ𝔥𝔞𝔱𝔅𝔬𝔱
4️⃣<<<==>>> 𝔊𝔓𝔖 𝔗𝔯𝔞𝔠𝔨𝔦𝔫𝔤
5️⃣<<<==>>> 𝔗𝔢𝔩𝔢𝔤𝔯𝔞𝔭𝔥 𝔊𝔢𝔫𝔢𝔯𝔞𝔱𝔬𝔯
6️⃣<<<==>>> 𝔘𝔰𝔢𝔯 ℑ𝔫𝔣𝔬
7️⃣<<<==>>> 𝔗𝔞𝔤𝔞𝔩𝔩
8️⃣<<<==>>> 𝔖𝔭𝔢𝔢𝔡 𝔗𝔢𝔰𝔱𝔢𝔯
9️⃣<<<==>>> 𝔑𝔦𝔤𝔥𝔱 𝔐𝔬𝔡𝔢
🔟<<<===>>> 𝔐𝔲𝔱𝔢 𝔓𝔬𝔴𝔢𝔯

◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊
*⚫ 𝔗𝔬 𝔤𝔢𝔱 𝔪𝔬𝔯𝔢 𝔦𝔫𝔣𝔬𝔯𝔪𝔞𝔱𝔦𝔬𝔫 𝔞𝔟𝔬𝔲𝔱 𝔪𝔢 𝔞𝔫𝔡 𝔪𝔶 𝔣𝔢𝔞𝔱𝔲𝔯𝔢𝔰 𝔰𝔬 𝔭𝔩𝔢𝔞𝔰𝔢 𝔠𝔩𝔦𝔠𝔨 𝔬𝔫 𝔥𝔢𝔩𝔭 𝔟𝔲𝔱𝔱𝔬𝔫.*
*©️ ɮʟǟƈӄʍǟʍɮǟ*
"""

buttons = [
    [
        InlineKeyboardButton(
            text="ǟɖɖ ʍɛ ɨռ ʏօʊʀ ɢʀօʊք 🤩",
            url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
        ),
    ],
    [
        InlineKeyboardButton(text="ɦɛʟք & ƈօʍʍǟռɖֆ", callback_data="help_back"),
    ],
    [
        InlineKeyboardButton(text="🧑‍🤝‍🧑ռɛȶաօʀӄ 🧑‍🤝‍🧑", url=f"https://t.me/MAMBA_NETWORK_OFFICIAL"),
        InlineKeyboardButton(text="✨ ֆʊքքօʀȶ ✨", url=f"https://t.me/MAMBA_CHAT_OFFICIAL"),
        InlineKeyboardButton(text="✨ ƈօʊʀֆɛֆ ✨", url=f"https://t.me/MAMBA_COURSES"),
    ],
    [
        InlineKeyboardButton(text="😎 օառɛʀ 😎", url=f"https://t.me/ITZ_ME_BLACKMAMBA"),
        InlineKeyboardButton(text="☁️ ʀɛքօ ☁️", url=f"https://blackmambaofficial.in"),
    ],
]

HELP_STRINGS = f"""
*» {BOT_NAME} 𝔈𝔵𝔢𝔠𝔲𝔱𝔦𝔫𝔤 𝔉𝔢𝔞𝔱𝔲𝔯𝔢𝔰*

➲ /start : 𝔖𝔱𝔞𝔯𝔱 𝔪𝔢 | 𝔄𝔠𝔠𝔬𝔯𝔡𝔦𝔫𝔤 𝔱𝔬 𝔪𝔢 𝔶𝔬𝔲 𝔥𝔞𝔳𝔢 𝔞𝔩𝔯𝔢𝔞𝔡𝔶 𝔡𝔬𝔫𝔢 𝔦𝔱..
➲ /help  : 𝔄𝔳𝔞𝔦𝔩𝔞𝔟𝔩𝔢 𝔠𝔬𝔪𝔪𝔞𝔫𝔡 𝔖𝔢𝔠𝔱𝔦𝔬𝔫.
  ‣ ɪɴ ᴘᴍ : 𝔚𝔦𝔩𝔩 𝔰𝔢𝔫𝔡 𝔶𝔬𝔲 𝔥𝔢𝔩𝔭 𝔣𝔬𝔯 𝔞𝔩𝔩 𝔰𝔲𝔭𝔭𝔬𝔯𝔱𝔢𝔡 𝔪𝔬𝔡𝔲𝔩𝔢𝔰.
  ‣ ɪɴ ɢʀᴏᴜᴘ : 𝔚𝔦𝔩𝔩 𝔡𝔦𝔯𝔢𝔠𝔱𝔩𝔶 𝔶𝔬𝔲 𝔱𝔬 𝔓𝔐, 𝔴𝔦𝔱𝔥 𝔞𝔩𝔩 𝔱𝔥𝔞𝔱 𝔥𝔢𝔩𝔭 𝔐𝔬𝔡𝔲𝔩𝔢𝔰."""

IMPORTED = {}
MIGRATEABLE = []
HELPABLE = {}
STATS = []
USER_INFO = []
DATA_IMPORT = []
DATA_EXPORT = []
CHAT_SETTINGS = {}
USER_SETTINGS = {}

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("FallenRobot.modules." + module_name)
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__

    if imported_module.__mod_name__.lower() not in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception("Can't have two modules with the same name! Please change one")

    if hasattr(imported_module, "__help__") and imported_module.__help__:
        HELPABLE[imported_module.__mod_name__.lower()] = imported_module

    # Chats to migrate on chat_migrated events
    if hasattr(imported_module, "__migrate__"):
        MIGRATEABLE.append(imported_module)

    if hasattr(imported_module, "__stats__"):
        STATS.append(imported_module)

    if hasattr(imported_module, "__user_info__"):
        USER_INFO.append(imported_module)

    if hasattr(imported_module, "__import_data__"):
        DATA_IMPORT.append(imported_module)

    if hasattr(imported_module, "__export_data__"):
        DATA_EXPORT.append(imported_module)

    if hasattr(imported_module, "__chat_settings__"):
        CHAT_SETTINGS[imported_module.__mod_name__.lower()] = imported_module

    if hasattr(imported_module, "__user_settings__"):
        USER_SETTINGS[imported_module.__mod_name__.lower()] = imported_module


# do not async
def send_help(chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    dispatcher.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
        reply_markup=keyboard,
    )


@run_async
def start(update: Update, context: CallbackContext):
    args = context.args
    uptime = get_readable_time((time.time() - StartTime))
    if update.effective_chat.type == "private":
        if len(args) >= 1:
            if args[0].lower() == "help":
                send_help(update.effective_chat.id, HELP_STRINGS)
            elif args[0].lower().startswith("ghelp_"):
                mod = args[0].lower().split("_", 1)[1]
                if not HELPABLE.get(mod, False):
                    return
                send_help(
                    update.effective_chat.id,
                    HELPABLE[mod].__help__,
                    InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="◁", callback_data="help_back")]]
                    ),
                )

            elif args[0].lower() == "markdownhelp":
                IMPORTED["Exᴛʀᴀs"].markdown_help_sender(update)
            elif args[0].lower().startswith("stngs_"):
                match = re.match("stngs_(.*)", args[0].lower())
                chat = dispatcher.bot.getChat(match.group(1))

                if is_user_admin(chat, update.effective_user.id):
                    send_settings(match.group(1), update.effective_user.id, False)
                else:
                    send_settings(match.group(1), update.effective_user.id, True)

            elif args[0][1:].isdigit() and "rᴜʟᴇs" in IMPORTED:
                IMPORTED["rᴜʟᴇs"].send_rules(update, args[0], from_pm=True)

        else:
            first_name = update.effective_user.first_name
            update.effective_message.reply_sticker(
                "CAACAgUAAxkBAAJYsmLWRvm70cE-mmxSNCovEf4v1ueJAAIcCAACbMK4VuL4EmZEkq8WKQQ"
            )
            update.effective_message.reply_text(
                PM_START_TEXT.format(escape_markdown(first_name), BOT_NAME),
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=ParseMode.MARKDOWN,
                timeout=60,
            )
    else:
        update.effective_message.reply_photo(
            START_IMG,
            caption="ℑ 𝔞𝔪 𝔞𝔩𝔦𝔳𝔢 𝔟𝔞𝔟𝔶 !\n<b>ℑ 𝔡𝔦𝔡𝔫'𝔱 𝔰𝔩𝔢𝔭𝔱 𝔰𝔦𝔫𝔠𝔢​:</b> <code>{}</code>".format(
                uptime
            ),
            parse_mode=ParseMode.HTML,
        )


def error_handler(update, context):
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    LOGGER.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    message = (
        "An exception was raised while handling an update\n"
        "<pre>update = {}</pre>\n\n"
        "<pre>{}</pre>"
    ).format(
        html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False)),
        html.escape(tb),
    )

    if len(message) >= 4096:
        message = message[:4096]
    # Finally, send the message
    context.bot.send_message(chat_id=OWNER_ID, text=message, parse_mode=ParseMode.HTML)


# for test purposes
def error_callback(update: Update, context: CallbackContext):
    error = context.error
    try:
        raise error
    except Unauthorized:
        print("no nono1")
        print(error)
        # remove update.message.chat_id from conversation list
    except BadRequest:
        print("no nono2")
        print("BadRequest caught")
        print(error)

        # handle malformed requests - read more below!
    except TimedOut:
        print("no nono3")
        # handle slow connection problems
    except NetworkError:
        print("no nono4")
        # handle other connection problems
    except ChatMigrated as err:
        print("no nono5")
        print(err)
        # the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError:
        print(error)
        # handle all other telegram related errors


@run_async
def help_button(update, context):
    query = update.callback_query
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)

    print(query.message.chat.id)

    try:
        if mod_match:
            module = mod_match.group(1)
            text = (
                "» *𝕬𝖛𝖆𝖎𝖑𝖆𝖇𝖑𝖊 𝖈𝖔𝖒𝖒𝖆𝖓𝖉𝖘 𝖋𝖔𝖗* *{}* :\n".format(
                    HELPABLE[module].__mod_name__
                )
                + HELPABLE[module].__help__
            )
            query.message.edit_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="⇦", callback_data="help_back")]]
                ),
            )

        elif prev_match:
            curr_page = int(prev_match.group(1))
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(curr_page - 1, HELPABLE, "help")
                ),
            )

        elif next_match:
            next_page = int(next_match.group(1))
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(next_page + 1, HELPABLE, "help")
                ),
            )

        elif back_match:
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, HELPABLE, "help")
                ),
            )

        context.bot.answer_callback_query(query.id)

    except BadRequest:
        pass


@run_async
def Fallen_about_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "fallen_":
        uptime = get_readable_time((time.time() - StartTime))
        query.message.edit_text(
            text=f"*ℌ𝔢𝔶𝔞,*🥀\n  *ℑ 𝔞𝔪 {BOT_NAME}*"
            "\n*𝔗𝔥𝔦𝔰 𝔦𝔰 𝔓𝔬𝔴𝔢𝔯𝔣𝔲𝔩𝔩 𝔤𝔯𝔬𝔲𝔭 𝔪𝔞𝔫𝔞𝔤𝔢𝔪𝔢𝔫𝔱 𝔟𝔬𝔱. 𝔗𝔥𝔦𝔰 𝔟𝔬𝔱 𝔥𝔢𝔩𝔭𝔰 𝔶𝔬𝔲 𝔱𝔬𝔬 𝔪𝔞𝔫𝔞𝔤𝔢 𝔶𝔬𝔲𝔯 𝔤𝔯𝔬𝔲𝔭. 𝔗𝔥𝔦𝔰 𝔟𝔬𝔱 𝔴𝔦𝔩𝔩 𝔟𝔢 𝔭𝔯𝔬𝔱𝔢𝔠𝔱 𝔶𝔬𝔲𝔯 𝔤𝔯𝔬𝔲𝔭 𝔣𝔯𝔬𝔪 𝔰𝔠𝔞𝔪𝔪𝔢𝔯𝔰 𝔞𝔫𝔡 𝔖𝔭𝔞𝔪𝔪𝔢𝔯𝔰.*"
            "\n*𝔚𝔯𝔦𝔱𝔱𝔢𝔫 𝔦𝔫 𝔭𝔶𝔱𝔥𝔬𝔫 𝔴𝔦𝔱𝔥 𝔖𝔮𝔩𝔞𝔩𝔠𝔥𝔢𝔪𝔶 𝔞𝔫𝔡 𝔐𝔞𝔫𝔤𝔬𝔇𝔟 𝔞𝔰 𝔇𝔞𝔱𝔞𝔟𝔞𝔰𝔢..*"
            "\n\n────────────────────"
            f"\n*➻ 𝔘𝔭𝔱𝔦𝔪𝔢 »* {uptime}"
            f"\n*➻ 𝔘𝔰𝔢𝔯𝔰 »* {sql.num_users()}"
            f"\n*➻ ℭ𝔥𝔞𝔱𝔰 »* {sql.num_chats()}"
            "\n────────────────────"
            "\n\n➲  ℑ 𝔠𝔞𝔫 ℜ𝔢𝔰𝔱𝔯𝔦𝔠𝔱 𝔱𝔥𝔢 𝔲𝔰𝔢𝔯𝔰."
            "\n➲  ℑ 𝔥𝔞𝔳𝔢 𝔞𝔫 𝔞𝔡𝔳𝔞𝔫𝔠𝔢𝔡 𝔞𝔫𝔱𝔦-𝔣𝔩𝔬𝔬𝔡 𝔣𝔢𝔞𝔱𝔲𝔯𝔢𝔰."
            "\n➲  ℑ 𝔠𝔞𝔫 𝔤𝔯𝔢𝔢𝔱 𝔱𝔥𝔢 𝔲𝔰𝔢𝔯𝔰 𝔴𝔦𝔱𝔥 𝔠𝔲𝔰𝔱𝔬𝔪𝔦𝔰𝔞𝔟𝔩𝔢 𝔴𝔢𝔩𝔠𝔬𝔪𝔢 𝔪𝔢𝔰𝔰𝔞𝔤𝔢𝔰 𝔞𝔫𝔡 𝔢𝔳𝔢𝔫 𝔞 𝔤𝔯𝔬𝔲𝔭 𝔯𝔲𝔩𝔢.."
            "\n➲  ℑ 𝔠𝔞𝔫 𝔴𝔞𝔯𝔫 𝔲𝔰𝔢𝔯𝔰 𝔲𝔫𝔱𝔦𝔩 𝔱𝔥𝔢𝔶 𝔯𝔢𝔞𝔠𝔥 𝔪𝔞𝔵 𝔴𝔞𝔯𝔫𝔰, 𝔴𝔦𝔱𝔥 𝔢𝔞𝔠𝔥 𝔭𝔯𝔢𝔡𝔢𝔣𝔦𝔫𝔢𝔡 𝔞𝔠𝔱𝔦𝔬𝔫𝔰 𝔰𝔲𝔠𝔥 𝔞𝔰 𝔟𝔞𝔫, 𝔪𝔲𝔱𝔢, 𝔨𝔦𝔠𝔨 𝔢𝔱𝔠.."
            "\n➲  ℑ 𝔥𝔞𝔳𝔢 𝔞 𝔫𝔬𝔱𝔢 𝔨𝔢𝔢𝔭𝔦𝔫𝔤 𝔰𝔶𝔰𝔱𝔢𝔪, 𝔟𝔩𝔞𝔠𝔨𝔩𝔦𝔰𝔱𝔰 𝔞𝔫𝔡 𝔢𝔳𝔢𝔫 𝔭𝔯𝔢𝔡𝔢𝔱𝔢𝔯𝔪𝔦𝔫𝔢𝔡 𝔯𝔢𝔭𝔩𝔦𝔢𝔰 𝔬𝔫 𝔠𝔢𝔯𝔱𝔞𝔦𝔫 𝔨𝔢𝔶𝔴𝔬𝔯𝔡𝔰."
            f"\n\n➻ ℭ𝔩𝔦𝔠𝔨 𝔬𝔫 𝔱𝔥𝔢 𝔟𝔲𝔱𝔱𝔬𝔫 𝔤𝔦𝔳𝔢𝔫 𝔟𝔢𝔩𝔬𝔴 𝔣𝔬𝔯 𝔤𝔢𝔱𝔱𝔦𝔫𝔤 𝔟𝔞𝔰𝔦𝔠 𝔥𝔢𝔩𝔭 𝔞𝔫𝔡 𝔦𝔫𝔣𝔬 𝔞𝔟𝔬𝔲𝔱 {BOT_NAME}.",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="𝐒𝐮𝐩𝐩𝐨𝐫𝐭", callback_data="OfficialSelfGrowth"
                        ),
                        InlineKeyboardButton(
                            text="𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬", callback_data="help_back"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫", url=f"tg://user?id={OWNER_ID}"
                        ),
                        InlineKeyboardButton(
                            text="𝐒𝐨𝐮𝐫𝐜𝐞",
                            callback_data="source_",
                        ),
                    ],
                    [
                        InlineKeyboardButton(text="⇦", callback_data="fallen_back"),
                    ],
                ]
            ),
        )
    elif query.data == "Gorrila_support":
        query.message.edit_text(
            text="*๏ ℭ𝔩𝔦𝔠𝔨 𝔬𝔫 𝔱𝔥𝔢 𝔟𝔲𝔱𝔱𝔬𝔫 𝔤𝔦𝔳𝔢𝔫 𝔟𝔢𝔩𝔬𝔴 𝔱𝔬 𝔤𝔢𝔱 𝔥𝔢𝔩𝔭 𝔞𝔫𝔡 𝔪𝔬𝔯𝔢 𝔦𝔫𝔣𝔬 𝔞𝔟𝔬𝔲𝔱 𝔪𝔢.*"
            f"\n\nℑ𝔣 𝔶𝔬𝔲 𝔣𝔦𝔫𝔡 𝔞𝔫𝔶 𝔟𝔲𝔤 𝔦𝔫 {BOT_NAME} 𝔬𝔯 𝔦𝔣 𝔶𝔬𝔲 𝔴𝔞𝔫𝔫𝔞 𝔤𝔦𝔳𝔢𝔫 𝔣𝔢𝔢𝔡𝔟𝔞𝔠𝔨 𝔞𝔟𝔬𝔲𝔱 𝔪𝔢 {BOT_NAME}, .",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="𝐒𝐮𝐩𝐩𝐨𝐫𝐭", url=f"https://t.me/MAMBA_FED"
                        ),
                        InlineKeyboardButton(
                            text="𝐔𝐩𝐝𝐚𝐭𝐞𝐬", url=f"https://t.me/MAMBA_FED_OFFICIAL"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="𝐏𝐫𝐨𝐠𝐫𝐚𝐦𝐦𝐞𝐫", url=f"https://t.me/MISS_PSYYCHO"
                        ),
                        InlineKeyboardButton(
                            text="𝐂𝐨𝐝𝐞",
                            url="https://www.pornhub.com",
                        ),
                    ],
                    [
                        InlineKeyboardButton(text="⇦", callback_data="fallen_"),
                    ],
                ]
            ),
        )
    elif query.data == "fallen_back":
        first_name = update.effective_user.first_name
        query.message.edit_text(
            PM_START_TEXT.format(escape_markdown(first_name), BOT_NAME),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.MARKDOWN,
            timeout=60,
            disable_web_page_preview=True,
        )


@run_async
def Source_about_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "source_":
        query.message.edit_text(
            text=f"""
*𝐻𝐸𝑀𝐿𝒪,
 𝐼 𝒜𝑀 {BOT_NAME},
𝓉𝑒𝓁𝑒𝑔𝓇𝒶𝓂 𝑔𝓇𝑜𝓊𝓅 𝓂𝒶𝓃𝒶𝑔𝑒𝓂𝑒𝓃𝓉 𝒷𝑜𝓉.*

🅣🅗🅘🅢 🅒🅞🅓🅔 🅘🅢 🅦🅡🅘🅣🅣🅔🅝 🅘🅝 🅟🅨🅣🅗🅞🅝 🅣🅗🅡🅞🅤🅖🅗  : [ᴛᴇʟᴇᴛʜᴏɴ](https://github.com/LonamiWebs/Telethon)
[ᵖʸʳᵒᵍʳᵃᵐ](https://github.com/pyrogram/pyrogram)
[ᵖʸᵗʰᵒⁿ-ᵗᵉˡᵉᵍʳᵃᵐ-ᵇᵒᵗ](https://github.com/python-telegram-bot/python-telegram-bot)
𝒜𝓃𝒹 𝓊𝓈𝒾𝓃𝑔 [𝒮𝓆𝓁𝒶𝓁𝒸𝒽𝑒𝓂𝓎](https://www.sqlalchemy.org) 𝒶𝓃𝒹 [𝓂𝒶𝓃𝑔𝑜](https://cloud.mongodb.com) ᴀs ᴅᴀᴛᴀʙᴀsᴇ.


*🅂🄾🅄🅁🄲🄴 🄲🄾🄳🄴 :* [ѕσυя¢є](https://www.pornhub.com)
*🄼🅈 🅈🄾🅄🅃🅄🄱🄴 🄲🄷🄰🄽🄽🄴🄻:*[уσυтυвє](www.youtube.com/channel/UC-fmEkPQ0J-o3X73g4XvnnQ)

{BOT_NAME} тнιѕ вσт ιѕ мαιηтαιηιηg ву вℓα¢кмαмвα αη∂ ℓι¢єη¢ιηg σƒ тнιѕ вσт ιѕ υη∂єя тнє [ℓι¢єη¢є](https://github.com/FantasticSukhi/GorillaRobot/blob/master/LICENSE).
© 𝕱𝖆𝖓𝖙𝖆𝖘𝖙𝖎𝖈𝕾𝖚𝖐𝖍𝖎✍ || [𝔖𝔲𝔭𝔭𝔬𝔯𝔱 𝔠𝔥𝔞𝔱](https://t.me/{SUPPORT_CHAT})|| 𝕹𝖔𝖙𝖊 :- 𝕴𝖋 𝖞𝖔𝖚 𝖜𝖆𝖓𝖙 𝖘𝖔𝖚𝖗𝖈𝖊 𝖈𝖔𝖉𝖊 𝖋𝖎𝖗𝖘𝖙𝖑𝖞 𝖉𝖔 𝖕𝖆𝖞𝖒𝖊𝖓𝖙 𝖜𝖍𝖎𝖈𝖍 𝖎𝖘 𝕽𝖘.𝟓𝟎𝟎𝟎 𝖆𝖓𝖉 𝖙𝖍𝖊𝖓 𝖘𝖊𝖓𝖉 𝖘𝖈𝖗𝖊𝖊𝖓𝖘𝖍𝖔𝖙 𝖎𝖋 𝖕𝖆𝖞𝖒𝖊𝖓𝖙 𝖎𝖘 𝖗𝖊𝖆𝖑𝖑𝖞 𝖉𝖔𝖓𝖊 𝖙𝖍𝖊𝖓 𝖘𝖔𝖚𝖗𝖈𝖊 𝖈𝖔𝖉𝖊 𝖎𝖘 𝖎𝖓 𝖞𝖔𝖚𝖗 𝖍𝖆𝖓𝖉 𝖔𝖙𝖍𝖊𝖗𝖜𝖎𝖘𝖊 𝖞𝖔𝖚 𝖋𝖔𝖗𝖌𝖊𝖙 𝖙𝖍𝖊 𝖘𝖔𝖚𝖗𝖈𝖊 𝖈𝖔𝖉𝖊✍.
""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="◁", callback_data="source_back")]]
            ),
        )
    elif query.data == "source_back":
        first_name = update.effective_user.first_name
        query.message.edit_text(
            PM_START_TEXT.format(escape_markdown(first_name), BOT_NAME),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.MARKDOWN,
            timeout=60,
            disable_web_page_preview=True,
        )


@run_async
def get_help(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    args = update.effective_message.text.split(None, 1)

    # ONLY send help in PM
    if chat.type != chat.PRIVATE:
        if len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
            module = args[1].lower()
            update.effective_message.reply_text(
                f"Contact me in PM to get help of {module.capitalize()}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="ʜᴇʟᴘ",
                                url="https://t.me/{}?start=ghelp_{}".format(
                                    context.bot.username, module
                                ),
                            )
                        ]
                    ]
                ),
            )
            return
        update.effective_message.reply_text(
            "» ¢нσσѕє αη∂ σρтιση ƒσя gєттιηg нєℓρ.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="σρєη ιη ∂м",
                            url="https://t.me/{}?start=help".format(
                                context.bot.username
                            ),
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="σρєη нєяє",
                            callback_data="help_back",
                        )
                    ],
                ]
            ),
        )
        return

    elif len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
        module = args[1].lower()
        text = (
            "Here is the available help for the *{}* module:\n".format(
                HELPABLE[module].__mod_name__
            )
            + HELPABLE[module].__help__
        )
        send_help(
            chat.id,
            text,
            InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="⇦", callback_data="help_back")]]
            ),
        )

    else:
        send_help(chat.id, HELP_STRINGS)


def send_settings(chat_id, user_id, user=False):
    if user:
        if USER_SETTINGS:
            settings = "\n\n".join(
                "*{}*:\n{}".format(mod.__mod_name__, mod.__user_settings__(user_id))
                for mod in USER_SETTINGS.values()
            )
            dispatcher.bot.send_message(
                user_id,
                "These are your current settings:" + "\n\n" + settings,
                parse_mode=ParseMode.MARKDOWN,
            )

        else:
            dispatcher.bot.send_message(
                user_id,
                "Seems like there aren't any user specific settings available :'(",
                parse_mode=ParseMode.MARKDOWN,
            )

    else:
        if CHAT_SETTINGS:
            chat_name = dispatcher.bot.getChat(chat_id).title
            dispatcher.bot.send_message(
                user_id,
                text="Which module would you like to check {}'s settings for?".format(
                    chat_name
                ),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )
        else:
            dispatcher.bot.send_message(
                user_id,
                "𒆜ֆɛɛʍֆ ʟɨӄɛ ȶɦɛʀɛ ǟʀɛռ'ȶ ǟռʏ ƈɦǟȶ ֆɛȶȶɨռɢֆ ǟʋǟɨʟǟɮʟɛ :'(\ռֆɛռɖ ȶɦɨֆ 𒆜 "
                "𒆜ɨռ ǟ ɢʀօʊք ƈɦǟȶ ʏօʊ'ʀɛ ǟɖʍɨռ ɨռ ȶօ ʄɨռɖ ɨȶֆ ƈʊʀʀɛռȶ ֆɛȶȶɨռɢֆ! 𒆜",
                parse_mode=ParseMode.MARKDOWN,
            )


@run_async
def settings_button(update: Update, context: CallbackContext):
    query = update.callback_query
    user = update.effective_user
    bot = context.bot
    mod_match = re.match(r"stngs_module\((.+?),(.+?)\)", query.data)
    prev_match = re.match(r"stngs_prev\((.+?),(.+?)\)", query.data)
    next_match = re.match(r"stngs_next\((.+?),(.+?)\)", query.data)
    back_match = re.match(r"stngs_back\((.+?)\)", query.data)
    try:
        if mod_match:
            chat_id = mod_match.group(1)
            module = mod_match.group(2)
            chat = bot.get_chat(chat_id)
            text = "*{}* has the following settings for the *{}* module:\n\n".format(
                escape_markdown(chat.title), CHAT_SETTINGS[module].__mod_name__
            ) + CHAT_SETTINGS[module].__chat_settings__(chat_id, user.id)
            query.message.reply_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="⇦",
                                callback_data="stngs_back({})".format(chat_id),
                            )
                        ]
                    ]
                ),
            )

        elif prev_match:
            chat_id = prev_match.group(1)
            curr_page = int(prev_match.group(2))
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                "▄︻デɦɨ ȶɦɛʀɛ! ȶɦɛʀɛ ǟʀɛ զʊɨȶɛ ǟ ʄɛա ֆɛȶȶɨռɢֆ ʄօʀ {} - ɢօ ǟɦɛǟɖ ǟռɖ քɨƈӄ աɦǟȶ══━一 "
                "▄︻デʏօʊ'ʀɛ ɨռȶɛʀɛֆȶɛɖ ɨռ.══━一".format(chat.title),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        curr_page - 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif next_match:
            chat_id = next_match.group(1)
            next_page = int(next_match.group(2))
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                "▄︻デɦɨ ȶɦɛʀɛ! ȶɦɛʀɛ ǟʀɛ զʊɨȶɛ ǟ ʄɛա ֆɛȶȶɨռɢֆ ʄօʀ {} - ɢօ ǟɦɛǟɖ ǟռɖ քɨƈӄ աɦǟȶ══━一 "
                "▄︻デʏօʊ'ʀɛ ɨռȶɛʀɛֆȶɛɖ ɨռ.══━一.".format(chat.title),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        next_page + 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif back_match:
            chat_id = back_match.group(1)
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                text="▄︻デɦɨ ȶɦɛʀɛ! ȶɦɛʀɛ ǟʀɛ զʊɨȶɛ ǟ ʄɛա ֆɛȶȶɨռɢֆ ʄօʀ {} - ɢօ ǟɦɛǟɖ ǟռɖ քɨƈӄ աɦǟȶ══━一 "
                "▄︻デʏօʊ'ʀɛ ɨռȶɛʀɛֆȶɛɖ ɨռ.══━一.".format(escape_markdown(chat.title)),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )

        # ensure no spinny white circle
        bot.answer_callback_query(query.id)
        query.message.delete()
    except BadRequest as excp:
        if excp.message not in [
            "𝘔𝘦𝘴𝘴𝘢𝘨𝘦 𝘪𝘴 𝘯𝘰𝘵 𝘮𝘰𝘥𝘪𝘧𝘪𝘦𝘥",             
            "𝘘𝘶𝘦𝘳𝘺_𝘪𝘥_𝘪𝘯𝘷𝘢𝘭𝘪𝘥",             
            "𝘔𝘦𝘴𝘴𝘢𝘨𝘦 𝘤𝘢𝘯'𝘵 𝘣𝘦 𝘥𝘦𝘭𝘦𝘵𝘦𝘥",
        ]:
            LOGGER.exception("𝐄𝐱𝐜𝐞𝐩𝐭𝐢𝐨𝐧 𝐢𝐧 𝐬𝐞𝐭𝐭𝐢𝐧𝐠𝐬 𝐛𝐮𝐭𝐭𝐨𝐧. %s", str(query.data))


@run_async
def get_settings(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    msg = update.effective_message  # type: Optional[Message]

    # ONLY send settings in PM
    if chat.type != chat.PRIVATE:
        if is_user_admin(chat, user.id):
            text = "ᶜˡⁱᶜᵏ ʰᵉʳᵉ ᵗᵒ ᵍᵉᵗ ᵗʰⁱˢ ᶜʰᵃᵗ'ˢ ˢᵉᵗᵗⁱⁿᵍˢ, ᵃˢ ʷᵉˡˡ ᵃˢ ʸᵒᵘʳˢ."
            msg.reply_text(
                text,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="sᴇᴛᴛɪɴɢs",
                                url="t.me/{}?start=stngs_{}".format(
                                    context.bot.username, chat.id
                                ),
                            )
                        ]
                    ]
                ),
            )
        else:
            text = "♥ﮩ٨ـﮩﮩ٨ـﮩﮩ ¢ℓι¢к нєяє тσ ¢нє¢к уσυя ѕєттιηgѕ ﮩﮩـ٨ﮩﮩـ٨ﮩ♥."

    else:
        send_settings(chat.id, user.id, True)


def migrate_chats(update: Update, context: CallbackContext):
    msg = update.effective_message  # type: Optional[Message]
    if msg.migrate_to_chat_id:
        old_chat = update.effective_chat.id
        new_chat = msg.migrate_to_chat_id
    elif msg.migrate_from_chat_id:
        old_chat = msg.migrate_from_chat_id
        new_chat = update.effective_chat.id
    else:
        return

    LOGGER.info("♥ﮩ٨ـﮩﮩ٨ـﮩﮩ мιgяαтιηg ƒяσм ﮩﮩـ٨ﮩﮩـ٨ﮩ♥ %s, to %s", str(old_chat), str(new_chat))
    for mod in MIGRATEABLE:
        mod.__migrate__(old_chat, new_chat)

    LOGGER.info("Successfully migrated!")
    raise DispatcherHandlerStop


def main():
    if SUPPORT_CHAT is not None and isinstance(SUPPORT_CHAT, str):
        try:
            dispatcher.bot.send_photo(
                chat_id=f"@{SUPPORT_CHAT}",
                photo=START_IMG,
                caption=f"""
ㅤ🥀 {BOT_NAME} ɪs ᴀʟɪᴠᴇ ʙᴀʙʏ...

┏•❅────✧❅✦❅✧────❅•┓
ㅤ★ **𝖕𝖞𝖙𝖍𝖔𝖓✍ :** `{y()}`
ㅤ★ **𝖑𝖎𝖇𝖗𝖆𝖗𝖞✍ :** `{telever}`
ㅤ★ **𝖙𝖊𝖑𝖊𝖙𝖍𝖔𝖓✍ :** `{tlhver}`
ㅤ★ **𝖕𝖞𝖗𝖔𝖌𝖗𝖆𝖒✍ :** `{pyrover}`
  ★ **𝕺𝖜𝖓𝖊𝖗✍ :** `@SelfGrowthOnline`
┗•❅────✧❅✦❅✧────❅•┛""",
                parse_mode=ParseMode.MARKDOWN,
            )
        except Unauthorized:
            LOGGER.warning(
                f"Bot isn't able to send message to @{SUPPORT_CHAT}, go and check!"
            )
        except BadRequest as e:
            LOGGER.warning(e.message)

    start_handler = CommandHandler("start", start)

    help_handler = CommandHandler("help", get_help)
    help_callback_handler = CallbackQueryHandler(help_button, pattern=r"help_.*")

    settings_handler = CommandHandler("settings", get_settings)
    settings_callback_handler = CallbackQueryHandler(settings_button, pattern=r"stngs_")

    about_callback_handler = CallbackQueryHandler(
        Fallen_about_callback, pattern=r"fallen_"
    )
    source_callback_handler = CallbackQueryHandler(
        Source_about_callback, pattern=r"source_"
    )

    migrate_handler = MessageHandler(Filters.status_update.migrate, migrate_chats)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(about_callback_handler)
    dispatcher.add_handler(source_callback_handler)
    dispatcher.add_handler(settings_handler)
    dispatcher.add_handler(help_callback_handler)
    dispatcher.add_handler(settings_callback_handler)
    dispatcher.add_handler(migrate_handler)

    dispatcher.add_error_handler(error_callback)

    LOGGER.info("Using long polling.")
    updater.start_polling(timeout=15, read_latency=4, clean=True)

    if len(argv) not in (1, 3, 4):
        telethn.disconnect()
    else:
        telethn.run_until_disconnected()

    updater.idle()


if __name__ == "__main__":
    LOGGER.info("Successfully loaded modules: " + str(ALL_MODULES))
    telethn.start(bot_token=TOKEN)
    pbot.start()
    main()
