import asyncio, os
from telethon import TelegramClient, events, functions, errors

# Render ke environment variables se details uthane ke liye
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_USERNAME = os.environ.get("CHANNEL_USERNAME")

bot = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@bot.on(events.NewMessage(func=lambda e: e.is_group))
async def force_join(event):
    if event.is_private:
        return

    user_id = event.sender_id
    sender = await event.get_sender()
    first_name = sender.first_name if sender.first_name else "Dost"

    try:
        # Check membership
        await bot(functions.channels.GetParticipantRequest(
            channel=f'@{CHANNEL_USERNAME}',
            participant=user_id
        ))
    except errors.UserNotParticipantError:
        await event.delete()
        warning = await event.respond(
            f"🌟 **Namaste [{first_name}](tg://user?id={user_id})!**\n\n"
            f"Aapka hamare group mein swagat hai! ❤️\n\n"
            f"Aapse ek choti si guzarish hai, hamara official channel @{CHANNEL_USERNAME} join karna zaroori hai.\n\n"
            f"Join karne ke baad aap yahan message kar payenge! 🙏\n\n"
            f"__Ye message 30 seconds mein hatt jayega.__"
        )
        await asyncio.sleep(30)
        await warning.delete()
    except Exception as e:
        print(f"Error: {e}")

print("✅ Bot is running 24/7 on Render...")
bot.run_until_disconnected()
