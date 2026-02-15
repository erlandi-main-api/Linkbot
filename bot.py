from pyrogram import Client, filters
import sqlite3
import base64
import config

db = sqlite3.connect(config.DATABASE_NAME, check_same_thread=False)
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id TEXT NOT NULL,
    owner TEXT
)
""")
db.commit()

app = Client(
    name="filelinkbot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    in_memory=True
)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "\U0001F44B Selamat datang!\n\n"
        "Kirim file untuk membuat link share.\n"
        "Gunakan /help untuk bantuan."
    )

@app.on_message(filters.command("help"))
async def help_command(client, message):
    await message.reply_text(
        "\U0001F4D6 Bantuan Bot\n\n"
        "Kirim file -> bot akan buat link.\n"
        "Klik link -> bot kirim ulang file."
    )

@app.on_message(filters.private & (filters.document | filters.video | filters.photo))
async def save_file(client, message):

    if message.document:
        file_id = message.document.file_id
    elif message.video:
        file_id = message.video.file_id
    elif message.photo:
        file_id = message.photo.file_id
    else:
        return

    owner = message.from_user.first_name

    cursor.execute(
        "INSERT INTO files (file_id, owner) VALUES (?, ?)",
        (file_id, owner)
    )
    db.commit()

    file_db_id = cursor.lastrowid
    encoded = base64.urlsafe_b64encode(str(file_db_id).encode()).decode()

    bot_username = (await client.get_me()).username
    link = f"https://t.me/{bot_username}?start={encoded}"

    await message.reply_text(
        "\u2705 File berhasil disimpan!\n\n"
        f"\U0001F517 Here is your link:\n{link}"
    )

@app.on_message(filters.command("start") & filters.private)
async def start_with_link(client, message):

    if len(message.command) > 1:
        try:
            encoded = message.command[1]
            decoded_id = base64.urlsafe_b64decode(encoded).decode()

            cursor.execute("SELECT file_id FROM files WHERE id = ?", (decoded_id,))
            result = cursor.fetchone()

            if result:
                await message.reply_document(result[0])
            else:
                await message.reply_text("\u274C File tidak ditemukan.")
        except:
            await message.reply_text("\u274C Link tidak valid.")

print("Bot berjalan...")
app.run()
