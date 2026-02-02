import os
from pyrogram import Client, filters, InlineQueryResultArticle, InputTextMessageContent
import yt_dlp

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    print("❌ Set BOT_TOKEN in Railway!")
    exit(1)

app = Client("tamil-bot", bot_token=TOKEN)

ydl_opts_search = {
    'quiet': True, 'extract_flat': True, 'playlist_items': '1-15'
}

ydl_opts_download = {
    'format': 'bestaudio/best', 'outtmpl': 'song.%(ext)s',
    'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '320'}],
    'retries': 5, 'fragment_retries': 5, 'socket_timeout': 20, 'extractor_retries': 3
}

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("🎵 **Tamil MP3 Bot**\n\n`@yourbot leo` → All songs → Click → MP3!")

@app.on_inline_query()
async def inline_search(client, query):
    text = query.query.lower()
    playlist = "https://www.youtube.com/playlist?list=PL4qyD_w1ZqEMb4H3sY5gP0l0Kq0kY0kY0"
    
    if "leo" in text:
        try:
            with yt_dlp.YoutubeDL(ydl_opts_search) as ydl:
                data = ydl.extract_info(playlist, download=False)
                entries = data.get('entries', [])[:10]
            
            results = []
            for i, entry in enumerate(entries):
                title = entry.get('title', 'Unknown')[:50]
                vid = entry.get('id')
                results.append(InlineQueryResultArticle(
                    id=str(i), title=title,
                    thumb_url=f"https://img.youtube.com/vi/{vid}/hqdefault.jpg",
                    input_message_content=InputTextMessageContent(f"https://youtu.be/{vid}")
                ))
            await query.answer(results)
        except: pass

@app.on_message(filters.text & filters.private)
async def download(client, message):
    if "youtube.com" in message.text or "youtu.be" in message.text:
        await message.reply("⏳ MP3...")
        try:
            with yt_dlp.YoutubeDL(ydl_opts_download) as ydl:
                ydl.download([message.text])
            await message.reply_audio("song.mp3", caption="✅ 320kbps")
            os.remove("song.mp3")
        except Exception as e:
            await message.reply(f"❌ {str(e)}")

print("🚀 Bot starting...")
app.run()
