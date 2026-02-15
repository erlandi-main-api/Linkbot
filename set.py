import os

if os.path.exists("config.py"):
    print("Config sudah ada.")
    exit()

print("=== SETUP BOT ===")

api_id = input("Masukkan API_ID: ")
api_hash = input("Masukkan API_HASH: ")
bot_token = input("Masukkan BOT_TOKEN: ")

with open("config.py", "w") as f:
    f.write(f"API_ID = {api_id}\n")
    f.write(f"API_HASH = '{api_hash}'\n")
    f.write(f"BOT_TOKEN = '{bot_token}'\n")
    f.write("DATABASE_NAME = 'files.db'\n")

print("Config berhasil dibuat.")
print("Sekarang jalankan: python3 bot.py")
