import json
import time
from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    ChatPermissions,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
#from pyrobot import COMMAND_HAND_LER, WARN_DATA_ID, WARN_SETTINGS_ID
from plugins.New.warn import PyroBot
from plugins.New.admin_check import (
    admin_check,  # TODO: remove in next version
)
from plugins.New.cust_p_filters import admin_fliter
from datetime import datetime, timedelta


# the logging things
import logging

from plugins.New.sample_config import Config
from info import ADMINS, API_ID, API_HASH, BOT_TOKEN

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


class PyroBot(Client):
    filterstore: Dict[str, Dict[str, str]] = defaultdict(dict)
    warndatastore: Dict[str, Dict[str, Union[str, int, List[str]]]] = defaultdict(dict)
    warnsettingsstore: Dict[str, str] = defaultdict(dict)

    def __init__(self):
        name = self.__class__.__name__.lower()
        super().__init__(
            name="PyroGramBot",
            plugins=dict(root=f"{name}/plugins"),
            workdir=TMP_DOWNLOAD_DIRECTORY,
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            parse_mode=ParseMode.HTML,
            sleep_threshold=60,
            in_memory=True
        )

COMMAND_HAND_LER = Config.COMMAND_HAND_LER
WARN_DATA_ID = int(Config.WARN_DATA_ID)
WARN_SETTINGS_ID = int(Config.WARN_SETTINGS_ID)
TMP_DOWNLOAD_DIRECTORY = TMP_DOWNLOAD_DIRECTORY


@PyroBot.on_message(
    filters.command(["warnuser", "warn"], COMMAND_HAND_LER) & admin_fliter
)
async def warn_user(client: PyroBot, msg: Message):
    chat_id = str(msg.chat.id)

    replied = msg.reply_to_message
    if not replied:
        return

    if chat_id not in client.warndatastore:
        client.warndatastore[chat_id] = {}

    DATA = client.warndatastore[chat_id]

    user_id = str(replied.from_user.id)
    mention = f"<a href='tg://user?id={user_id}'>"
    mention += replied.from_user.first_name
    mention += "</a>"

    if replied.from_user.is_self:
        await msg.reply_text("ഞാൻ സ്വയം താക്കീത്‌ നൽകാൻ പോകുന്നില്ല")
        return

    if await admin_check(replied):
        await msg.reply("User is Admin, Cannot Warn.")
        return

    if len(msg.command) < 2:
        await msg.reply("Give a reason to warn him.")
        return

    _, reason = msg.text.split(maxsplit=1)

    if chat_id not in client.warnsettingsstore:
        client.warnsettingsstore[chat_id] = {"WARN_LIMIT": 5, "WARN_MODE": "kick"}
    w_s = client.warnsettingsstore[chat_id]
    w_l = w_s["WARN_LIMIT"]
    w_m = w_s["WARN_MODE"]

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "ഈ താക്കീത്‌ നീക്കംചെയ്യുക",
                    callback_data=f"rmwarn_{user_id}_{msg.from_user.id}",
                )
            ]
        ]
    )

    if not DATA.get(user_id):
        w_d = {"limit": 1, "reason": [reason]}
        DATA[user_id] = w_d  # warning data
        reply_text = f"#Warned\n{mention} has 1/{w_l} warnings.\n"
        reply_text += f"<u>Reason</u>: {reason}"
        await replied.reply_text(reply_text, reply_markup=keyboard)
    else:
        p_l = DATA[user_id]["limit"]  # previous limit
        nw_l = p_l + 1  # new limit
        if nw_l >= w_l:
            if w_m == "ban":
                await msg.chat.ban_member(int(user_id))
                exec_str = "BANNED"
            elif w_m == "kick":
                await msg.chat.ban_member(int(user_id), until_date=datetime.now() + timedelta(seconds=75))
                exec_str = "KICKED"
            elif w_m == "mute":
                await msg.chat.restrict_member(int(user_id), ChatPermissions())
                exec_str = "MUTED"
            reason = "\n".join(DATA[user_id]["reason"]) + "\n" + str(reason)
            await msg.reply(
                f"#WARNED_{exec_str}\n"
                f"{exec_str} User: {mention}\n"
                f"Warn Counts: {w_l}/{w_l} Warnings\n"
                f"Reason: {reason}"
            )
            DATA.pop(user_id)

        else:
            DATA[user_id]["limit"] = nw_l
            DATA[user_id]["reason"].append(reason)
            r_t = f"#Warned\n{mention} has {nw_l}/{w_l} warnings.\n"
            r_t += f"<u>Reason</u>: {reason}"  # r_t = reply text
            await replied.reply_text(r_t, reply_markup=keyboard)

    client.warndatastore[chat_id] = DATA
    await client.save_public_store(WARN_DATA_ID, json.dumps(client.warndatastore))
    client.warnsettingsstore[chat_id] = w_s
    await client.save_public_store(
        WARN_SETTINGS_ID, json.dumps(client.warnsettingsstore)
    )
