import os
from pyrogram import Client, filters
from mega import Mega

# Yahan apni Telegram API ID, API Hash aur Bot Token dalein
API_ID = "39689089"  # Integer mein (e.g., 1234567)
API_HASH = "d23063ec3a2d899c60bd9d64bf3f7826"  # String mein
BOT_TOKEN = "8793293236:AAH1dVIRjlY7dGNNsocG8YZUqOAkG0p09Jo" # BotFather se mila token

# Pyrogram Client setup
app = Client("mega_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# MEGA anonymous login
mega = Mega()
m = mega.login()

@app.on_message(filters.regex(r"https://mega.nz/.*"))
async def handle_mega_link(client, message):
    url = message.text
    status_msg = await message.reply_text("⏳ MEGA se download ho raha hai... Kripya wait karein.")
    
    try:
        # MEGA link se server/laptop par file download karna
        file_path = m.download_url(url)
        
        await status_msg.edit_text("⏳ Telegram par upload ho raha hai...")
        
        # File ko Telegram par as a document upload karna
        await client.send_document(
            chat_id=message.chat.id,
            document=file_path,
            caption="✅ File successfully upload ho gayi!"
        )
        
        # Upload hone ke baad system se temporary file delete karna
        os.remove(file_path)
        await status_msg.delete()
        
    except Exception as e:
        await status_msg.edit_text(f"❌ Error aaya: {e}")

if __name__ == "__main__":
    print("Bot is running...")
    app.run()
