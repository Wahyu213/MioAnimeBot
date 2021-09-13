# To all kangers, You Dare kang this file and come asking for Not working in Tangent
# this is all a test

from pyrogram import filters

from EmiliaAnimeBot.arqclient import arq
from EmiliaAnimeBot import USERBOT_PREFIX, DEV_USERS, emiliaub


@app2.on_message(
    filters.command("q", prefixes=USERBOT_PREFIX)
    & filters.user(DEV_USERS)
)
@app.on_message(filters.command("q") & ~filters.private)
@capture_err
async def quotly_func(client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text(
            "Reply to a message to quote it."
        )
    if not message.reply_to_message.text:
        return await message.reply_text(
            "Replied message has no text, can't quote it."
        )
    m = await message.reply_text("Quoting Messages")
    if len(message.command) < 2:
        messages = [message.reply_to_message]

    elif len(message.command) == 2:
        arg = isArgInt(message)
        if arg[0]:
            if arg[1] < 2 or arg[1] > 10:
                return await m.edit("Argument must be between 2-10.")

            count = arg[1]

            messages = [
                i
                for i in await client.get_messages(
                    message.chat.id,
                    range(
                        message.reply_to_message.message_id,
                        message.reply_to_message.message_id + count,
                    ),
                    replies=0,
                )
                if not i.empty
            ]
        else:
            if getArg(message) != "r":
                return await m.edit(
                    "Incorrect Argument, Pass **'r'** or **'INT'**, **EX:** __/q 2__"
                )
            reply_message = await client.get_messages(
                message.chat.id,
                message.reply_to_message.message_id,
                replies=1,
            )
            messages = [reply_message]
    else:
        await m.edit(
            "Incorrect argument, check quotly module in help section."
        )
        return
    try:
        if not message:
            return await m.edit("Something went wrong.")

        sticker = await quotify(messages)
        if not sticker[0]:
            await message.reply_text(sticker[1])
            return await m.delete()
        sticker = sticker[1]
        await message.reply_sticker(sticker)
        await m.delete()
        sticker.close()
    except Exception as e:
        await m.edit(
            "Something went wrong while quoting messages,"
            + " This error usually happens when there's a "
            + " message containing something other than text,"
            + " or one of the messages in-between are deleted."
        )
        e = format_exc()
        print(e)
