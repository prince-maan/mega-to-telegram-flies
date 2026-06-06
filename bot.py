import os
import asyncio
import threading
import shutil
from pyrogram import Client, filters
from mega import Mega
from flask import Flask

# --- Python Event Loop Fix ---
try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

# --- Dummy Web Server (Render Free Plan Ke Liye) ---
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Bot is running perfectly!"

def run_web():
    port = int(os.environ.get("PORT", 8000))
    web_app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = threading.Thread(target=run_web)
    t.start()
# -----------------------------------------------------------------

# Aapki API aur Bot Details
API_ID = "39689089"
API_HASH = "d23063ec3a2d899c60bd9d64bf3f7826"
BOT_TOKEN = "8793293236:AAH1dVIRjlY7dGNNsocG8YZUqOAkG0p09Jo"

app = Client("mega_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
mega = Mega()

# /start command par message
@app.on_message(filters.command("start"))
async def start_msg(client, message):
    await message.reply_text("Hello Prince! Main ready hoon. Mujhe MEGA ka file ya folder link bhejiye.")

@app.on_message(filters.regex(r"https://mega\.nz/.*"))
async def handle_mega_link(client, message):
    url = message.text
    status_msg = await message.reply_text("⏳ MEGA Link process ho raha hai... Kripya wait karein.")
    
    # Har download ke liye ek naya temporary folder banayenge
    temp_dir = f"./temp_{message.message_id}"
    os.makedirs(temp_dir, exist_ok=True)
    
    try:
        # MEGA Anonymous Login
        m = mega.login()
        
        await status_msg.edit_text("⏳ File/Folder Server par download ho raha hai...")
        # Link ko temp_dir ke andar download karna
        m.download_url(url, dest_path=temp_dir)
        
        await status_msg.edit_text("⏳ Telegram par upload shuru ho raha hai...")
        
        # Temp folder ke andar check karna ki kya kya download hua hai
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                ext = os.path.splitext(file_path)[1].lower()
                
                # Agar Photo hai
                if ext in ['.jpg', '.jpeg', '.png', '.webp']:
                    await client.send_photo(chat_id=message.chat.id, photo=file_path)
                # Agar Video hai
                elif ext in ['.mp4', '.mkv', '.avi', '.mov']:
                    await client.send_video(chat_id=message.chat.id, video=file_path)
                # Agar koi aur document hai
                else:
                    await client.send_document(chat_id=message.chat.id, document=file_path)
        
        # Upload hone ke baad Render se kachra saaf (Delete) karna
        shutil.rmtree(temp_dir, ignore_errors=True)
        await status_msg.edit_text("✅ Sab kuch successfully upload ho gaya!")
        
    except Exception as e:
        await status_msg.edit_text(f"❌ Error aaya: {str(e)}")
        # Error aane par bhi server se temporary files delete karna zaroori hai
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    keep_alive()  # Server start
    print("Bot is running...")
    app.run()     # Bot start
