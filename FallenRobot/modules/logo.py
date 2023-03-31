import glob
import io
import os
import random

import requests
from PIL import Image, ImageDraw, ImageFont

from FallenRobot import BOT_NAME, BOT_USERNAME, OWNER_ID, telethn
from FallenRobot.events import register

LOGO_LINKS = [
    "https://graph.org/file/8e84fe3b5d518e7130162.jpg",
    "https://graph.org/file/81f4ebd496287372c4eb1.jpg",
    "https://graph.org/file/2b71b40bda5005544365b.jpg",
    "https://graph.org/file/2cad7ddd849c51388ef8a.jpg",
    "https://graph.org/file/6bb31f44eb1a8cd3b67bb.jpg",
    "https://graph.org/file/43de67aca1ddca462d323.jpg",
    "https://graph.org/file/7157fcfe610e2de4d2eb6.jpg",
    "https://graph.org/file/ab6e07cf174ce8cdba756.jpg",
    "https://graph.org/file/ef9582f1c2ab65af758d7.jpg",
    "https://graph.org/file/38a82c5a92efcc1d423cf.jpg",
    "https://graph.org/file/ec7ba29f4e97a7a8700de.jpg",
    "https://graph.org/file/dd52e0747438ec3752acd.jpg",
    "https://graph.org/file/b087cbaf60584c78235a9.jpg",
    "https://graph.org/file/18ddbef8c0513fefc064c.jpg",
]


@register(pattern="^/logo ?(.*)")
async def lego(event):
    quew = event.pattern_match.group(1)
    if event.sender_id != OWNER_ID and not quew:
        await event.reply(
            "ɢɪᴠᴇ sᴏᴍᴇ ᴛᴇxᴛ ᴛᴏ ᴄʀᴇᴀᴛᴇ ʟᴏɢᴏ ʙᴀʙʏ​ !\nExample : `/logo <BLACKMAMBA>`"
        )
        return
    pesan = await event.reply("**ᴄʀᴇᴀᴛɪɴɢ ʏᴏᴜʀ ʀᴇǫᴜᴇsᴛᴇᴅ ʟᴏɢᴏ ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ᴀ sᴇᴄ​...**")
    try:
        text = event.pattern_match.group(1)
        randc = random.choice(LOGO_LINKS)
        img = Image.open(io.BytesIO(requests.get(randc).content))
        draw = ImageDraw.Draw(img)
        image_widthz, image_heightz = img.size
        fnt = glob.glob("./FallenRobot/resources/fonts/*")
        randf = random.choice(fnt)
        font = ImageFont.truetype(randf, 120)
        w, h = draw.textsize(text, font=font)
        h += int(h * 0.21)
        image_width, image_height = img.size
        draw.text(
            ((image_widthz - w) / 2, (image_heightz - h) / 2),
            text,
            font=font,
            fill=(255, 255, 255),
        )
        x = (image_widthz - w) / 2
        y = (image_heightz - h) / 2 + 6
        draw.text(
            (x, y), text, font=font, fill="white", stroke_width=1, stroke_fill="black"
        )
        fname = "fallen.png"
        img.save(fname, "png")
        await telethn.send_file(
            event.chat_id,
            file=fname,
            caption=f"ʟᴏɢᴏ ɢᴇɴᴇʀᴀᴛᴇᴅ ʙʏ [{BOT_NAME}](https://t.me/{BOT_USERNAME})",
        )
        await pesan.delete()
        if os.path.exists(fname):
            os.remove(fname)
    except Exception:
        text = event.pattern_match.group(1)
        randc = random.choice(LOGO_LINKS)
        img = Image.open(io.BytesIO(requests.get(randc).content))
        draw = ImageDraw.Draw(img)
        image_widthz, image_heightz = img.size
        fnt = glob.glob("./FallenRobot/resources/fonts/*")
        randf = random.choice(fnt)
        font = ImageFont.truetype(randf, 120)
        w, h = draw.textsize(text, font=font)
        h += int(h * 0.21)
        image_width, image_height = img.size
        draw.text(
            ((image_widthz - w) / 2, (image_heightz - h) / 2),
            text,
            font=font,
            fill=(255, 255, 255),
        )
        x = (image_widthz - w) / 2
        y = (image_heightz - h) / 2 + 6
        draw.text(
            (x, y), text, font=font, fill="white", stroke_width=1, stroke_fill="black"
        )
        fname = "fallen.png"
        img.save(fname, "png")
        await telethn.send_file(
            event.chat_id,
            file=fname,
            caption=f"ʟᴏɢᴏ ɢᴇɴᴇʀᴀᴛᴇᴅ ʙʏ [{BOT_NAME}](https://t.me/{BOT_USERNAME})",
        )
        await pesan.delete()
        if os.path.exists(fname):
            os.remove(fname)


__mod_name__ = "Lᴏɢᴏ​"

__help__ = """
I can create some beautiful and attractive logo for your profile pics.

❍ /logo (Text) *:* Create a logo of your given text with random view.
"""
