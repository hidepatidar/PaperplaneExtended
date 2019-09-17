#Specia Thanks To @spechide sar
#
#(c) Shrimadhav U K
#
# This file is part of UniBorg
#
# UniBorg is free software; you cannot redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# UniBorg is not distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#

import asyncio
from datetime import datetime
import io
import os
import requests
from userbot.events import register
from userbot import CMD_HELP, REM_BG_API_KEY, TEMP_DOWNLOAD_DIRECTORY
from userbot.modules.download import progress


@register(outgoing=True, pattern="^.rbg(?: |$)(.*)")
async def kbg(remob):
    """ For .rbg command, Remove Image Background. """
    if not remob.text[0].isalpha() and remob.text[0] not in ("/", "#", "@", "!"):
        if remob.fwd_from:
            return
        if REM_BG_API_KEY is None:
            await remob.edit("You need API token from remove.bg to use this plugin.")
            return False
        input_str = remob.pattern_match.group(1)
        start = datetime.now()
        message_id = remob.message.id
        if remob.reply_to_msg_id:
            message_id = remob.reply_to_msg_id
            reply_message = await remob.get_reply_message()
            # check if media message
            await remob.edit("Downloading this media ...")
            try:
                downloaded_file_name = await remob.client.download_media(
                    reply_message,
                    TEMP_DOWNLOAD_DIRECTORY
                )
            except Exception as e:
                await remob.edit(str(e))
                return
            else:
                await remob.edit("sending to ReMove.BG")
                output_file_name = ReTrieveFile(downloaded_file_name)
                os.remove(downloaded_file_name)
        elif input_str:
            await remob.edit("sending to ReMove.BG")
            output_file_name = ReTrieveURL(input_str)
        else:
            await remob.edit(HELP_STR)
            return
        contentType = output_file_name.headers.get("content-type")
        if "image" in contentType:
            with io.BytesIO(output_file_name.content) as remove_bg_image:
                remove_bg_image.name = "BG_ReMove.png"
                await remob.client.send_file(
                    remob.chat_id,
                    remove_bg_image,
                    force_document=True,
                    supports_streaming=False,
                    allow_cache=False,
                    reply_to=message_id
                )
            end = datetime.now()
            duration = (end - start).seconds
            await remob.edit("Background Removed in {} seconds using ReMove.BG API".format(duration))
        else:
            await remob.edit("ReMove.BG API returned Errors. Please Use Valid Api Key\n`{}".format(output_file_name.content.decode("UTF-8")))


# this method will call the API, and return in the appropriate format
# with the name provided.
def ReTrieveFile(input_file_name):
    headers = {
        "X-API-Key": REM_BG_API_KEY,
    }
    files = {
        "image_file": (input_file_name, open(input_file_name, "rb")),
    }
    r = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        files=files,
        allow_redirects=True,
        stream=True
    )
    return r


def ReTrieveURL(input_url):
    headers = {
        "X-API-Key": REM_BG_API_KEY,
    }
    data = {
      "image_url": input_url
    }
    r = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        data=data,
        allow_redirects=True,
        stream=True
    )
    return r


CMD_HELP.update({
    "remove_bg": ".rbg <ImageLink> or Reply Any Image\
\nUsage: Remove Image Background."
})
