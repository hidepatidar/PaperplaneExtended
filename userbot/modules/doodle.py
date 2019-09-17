from search_engine_parser import GoogleSearch
from re import findall
from userbot.events import register
from userbot import CMD_HELP, BOTLOG, BOTLOG_CHATID


@register(outgoing=True, pattern=r"^.go (.*)")
async def gsearch(q_event):
    """ For .go command, do a Google search. """
    if not q_event.text[0].isalpha() and q_event.text[0] not in (
            "/", "#", "@", "!"):
        match = q_event.pattern_match.group(1)
        page = findall(r"page=\d+", match)
        try:
            page = page[0]
            page = page.replace("page=", "")
            match = match.replace("page=" + page[0], "")
        except IndexError:
            page = 1
        search_args = (str(match), int(page))
        gsearch = GoogleSearch()
        gresults = gsearch.search(*search_args)
        msg = ""
        for i in range(10):
            try:
                title = gresults["titles"][i]
                link = gresults["links"][i]
                msg += f"➺ {title}\n{link}\n\n"
            except IndexError:
                break
        await q_event.edit(
            "**Google Search Query :** `" + match + "`\n\n" + msg,
            link_preview = False
        )

        if BOTLOG:
            await q_event.client.send_message(
                BOTLOG_CHATID,
                "Google Search query `" + match + "` was executed successfully",
            )


CMD_HELP.update({
    'google': '.go <query>\
        \nUsage: Do a Google search.'
})
