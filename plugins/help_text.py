import logging
import time
import os
import sqlite3
import asyncio

if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
from pyrogram.errors import UserNotParticipant

from script import script
from plugins.rename_file import rename_doc

# Logging things
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


@Client.on_message(filters.command(["help"]))
async def help_user(bot, update):
    await bot.send_message(
      chat_id=update.chat.id,
      text=script.HELP_USER,
      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="⚜️ Support Group ⚜️", url="https://t.me/Nexa_bots")]]),
      parse_mode="html",
      disable_web_page_preview=True,
      reply_to_message_id=update.message_id
    )


@Client.on_message(filters.command(["start"]))
async def send_start(bot, update):
    await bot.send_message(
      chat_id=update.chat.id,
      text=script.START_TEXT.format(update.from_user.first_name),
      parse_mode="html",
      disable_web_page_preview=True,
      reply_to_message_id=update.message_id
    )


@Client.on_message(filters.command(["upgrade"]))
async def upgrade(bot, update):
    await bot.send_message(
      chat_id=update.chat.id,
      text=script.UPGRADE_TEXT,
      parse_mode="html",
      reply_to_message_id=update.message_id,
      disable_web_page_preview=True
    )

    
@Client.on_message(filters.private & (filters.document | filters.video | filters.audio | filters.voice | filters.video_note))
async def rename_cb(bot, update):
    file = update.document or update.video or update.audio or update.voice or update.video_note
    try:
        filename = file.file_name
    except:
        filename = "Not Available"
    await bot.send_message(
        chat_id=update.chat.id,
        text="<b>File Name:</b> <code>{}</code> \n\nPlease select your option 😊️".format(filename),
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="✍️ Rename This File ✍️", callback_data="rename_button")],
                                                [InlineKeyboardButton(text="❌️ CANCEL ❌️", callback_data="cancel_e")]]),
        parse_mode="html",
        reply_to_message_id=update.message_id,
        disable_web_page_preview=True   
    )   


async def cancel_extract(bot, update):
    await bot.send_message(
        chat_id=update.chat.id,
        text="Current Process Successfully Cancelled 😌️✅️",
    )
