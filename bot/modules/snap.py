import json

import requests
from bs4 import BeautifulSoup
from pyrogram import Client, filters

from bot import CMD, LOGGER

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
}
base_url = "https://story.snapchat.com/@"

START_TEXT = """Hello {} ✨

Send me Snapchat username to get Public Stories 👻.
"""


@Client.on_message(filters.command(CMD.START))
async def start(bot, update):
    await update.reply_text(
        text=START_TEXT.format(update.from_user.mention),
        disable_web_page_preview=True,
        quote=True,
    )


@Client.on_message(filters.text)
async def reply_shortens(bot, update):
    url = update.text
    S = base_url + url
    LOGGER.info(S)
    x = requests.get(S, headers=headers)
    soup = BeautifulSoup(x.content, "html.parser")
    snaps = soup.find(id="__NEXT_DATA__").string.strip()
    data = json.loads(snaps)
    try:
        for i in data["props"]["pageProps"]["story"]["snapList"]:
            await update.reply_document(
                document=i["snapUrls"]["mediaUrl"], caption="By: @Nexiou"
            )
    except KeyError:
        await update.reply_text(
            text="No Public Stories for past 24Hrs\n\n❌ OR INVALID USERNAME", quote=True
        )

    await update.reply_text(text="Done ✨ @Nexiuo", quote=True)
