#Special Thanks to @spechide Sar who found Unlimited Screencapture way

import io
import traceback
from datetime import datetime
from selenium import webdriver
from telethon import events
from userbot.events import register
from userbot import GOOGLE_CHROME_BIN, CMD_HELP


@register(pattern=r".sc (.*)", outgoing=True)
async def captur(shots):
    """ For .sc command, Capture any Site via Url."""
    if not shots.text[0].isalpha() and shots.text[0] not in ("/", "#", "@", "!"):
        if shots.fwd_from:
            return
        if GOOGLE_CHROME_BIN is None:
            await shots.edit("need to install Google Chrome. Module Stopping.")
            return
        await shots.edit("Processing ...")
        start = datetime.now()
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--ignore-certificate-errors')
            chrome_options.add_argument("--test-type")
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--window-size=1920x1080")
            # https://stackoverflow.com/a/53073789/4723940
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.binary_location = GOOGLE_CHROME_BIN
            await shots.edit("Processing 30%")
            driver = webdriver.Chrome(chrome_options=chrome_options)
            input_str = shots.pattern_match.group(1)
            driver.get(input_str)
            await shots.edit("Processing 50%")
            im_png = driver.get_screenshot_as_png()
            # saves screenshot of entire page
            driver.close()
            await shots.edit("Processing 90%")
            message_id = shots.message.id
            if shots.reply_to_msg_id:
                message_id = shots.reply_to_msg_id
            with io.BytesIO(im_png) as out_file:
                out_file.name = "screencapture.png"
                await shots.client.send_file(
                    shots.chat_id,
                    out_file,
                    caption=input_str,
                    force_document=True,
                    reply_to=message_id,
                    allow_cache=False,
                    silent=True
                )
            end = datetime.now()
            duration = (end - start).seconds
            await shots.edit(f"Screencaptured in {duration} seconds")
        except Exception:
            await shots.edit(traceback.format_exc())
           
           
CMD_HELP.update({
    "screencapture": ".sc <url>\
    \nUsage: Takes a screenshot of a website and sends the screenshot."
})
