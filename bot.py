import os
import asyncio
from telethon import TelegramClient, events

# Environment variables
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_USERNAME = os.environ.get("CHANNEL_USERNAME")

bot = TelegramClient('bot_session', API_ID, API_HASH)

@bot.on(events.NewMessage(func=lambda e: e.is_group))
async def check_user(event):
    if not CHANNEL_USERNAME:
        return
    try:
        from telethon.tl.functions.channels import GetParticipantRequest
        await bot(GetParticipantRequest(CHANNEL_USERNAME, event.sender_id))
    except Exception:
        await event.delete()
        user = await event.get_sender()
        name = user.first_name if user.first_name else "User"
        msg = f"Hey {name}! Please join @{CHANNEL_USERNAME} to message in this group."
        await event.respond(msg)

async def main():
    await bot.start(bot_token=BOT_TOKEN)
    print("✅ Bot is running 24/7 on Render...")
    await bot.run_until_disconnected()

if __name__ == '__main__':
    # Fix for Python 3.14+ event loop issue
    try:
        asyncio.run(main())
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
                    
