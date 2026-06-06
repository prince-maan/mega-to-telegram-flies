import os
from pyrogram import Client, filters
from mega import Mega
from flask import Flask
import threading

# --- Dummy Web Server (Render ko free plan par chalane ke liye) ---
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Bot is running perfectly on Render!"

def run_web():
    # Render automatically PORT deta hai, warna 8000 use karega
    port = int(os.environ.get("PORT", 8000))
    web_app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = threading.Thread(target=run_web)
    t.start()
# -----------------------------------------------------------------

# Yahan apni Telegram API ID, API Hash aur Bot Token dalein
API_ID = "39689089"
API_HASH = "d23063ec3a2d899c60bd9d64bf3f7826"
BOT_TOKEN = "8793293236:AAH1dVIRjlY7dGNNsocG8YZUqOAkG0p09Jo"

app = Client("mega_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
mega = Mega()
m = mega.login()

@app.on_message(filters.regex(r"https://mega\.nz/.*"))
async def handle_mega_link(client, message):
    url = message.text
    status_msg = await message.reply_text("⏳ MEGA se download ho raha hai... Kripya wait karein.")
    
    try:
        file_path = m.download_url(url)
        await status_msg.edit_text("⏳ Telegram par upload ho raha hai...")
        
        await client.send_document(
            chat_id=message.chat.id,
            document=file_path,
            caption="✅ File successfully upload ho gayi!"
        )
        
        os.remove(file_path)
        await status_msg.delete()
        
    except Exception as e:
        await status_msg.edit_text(f"❌ Error aaya: {e}")

if __name__ == "__main__":
    keep_alive()  # Yeh web server chalu karega taaki Render band na ho
    print("Bot is running...")
    app.run()     # Yeh Telegram bot chalu karega
