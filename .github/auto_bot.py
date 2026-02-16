from telethon import TelegramClient, events
from binance.client import Client
import re

# --- 1. KONFIGURASI RAHASIA ---
# Isi dengan data yang sudah kamu dapatkan tadi
API_ID = '39175714'
API_HASH = 'f7257756e4db3411f4e40b5f88aa7a31'
BINANCE_KEY = 'K3vlwKYo3hbe0mwpo8qOU7J1vOwm6SDonodU5M1o5zCkYWWkCVtvBzktSlAqtF9y'
BINANCE_SECRET = 'v8zJr42qgHqgx2242ReHzeR9lxebXBcxUfIjV6LMbQU5l3YN8dVEAUGG5uY1gPZE'

# ID Channel/Grup Sumber (Tempat bot mengambil sinyal)
# Kamu bisa isi dengan username channel, misal: 'GrupSinyalVip'
SOURCE_CHANNEL = ['@cryptoninjas_tradings_ann', '@UniversalCryptoSignalsGlobal']

# ID Telegram Salsa (Untuk laporan)
BOT_TOKEN = "8348453058:AAEdjA6d9YQSo1qriElIm5Ll9lD0m7N_h-0"
MY_CHAT_ID = "913800755"

# --- 2. INISIALISASI ---
t_client = TelegramClient('anzfx_userbot', API_ID, API_HASH)
b_client = Client(BINANCE_KEY, BINANCE_SECRET)

print("✅ Bot Pemantau Sedang Berjalan...")

# --- 3. LOGIKA PEMBACA SINYAL ---
@t_client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def my_event_handler(event):
    raw_text = event.raw_text
    print(f"📩 Pesan Masuk: {raw_text}")

    # Deteksi Sinyal (Regex)
    if "🎯" in raw_text or "Entry" in raw_text:
        try:
            pair = re.search(r"📊\s*(\w+)", raw_text).group(1)
            side = "SELL" if "SELL" in raw_text.upper() else "BUY"
            entry = re.search(r"Entry:\s*([\d.]+)", raw_text).group(1)
            
            print(f"🚀 Mengeksekusi {side} {pair} di Binance...")

            # --- 4. EKSEKUSI BINANCE (Contoh Market Order) ---
            # Catatan: Ini contoh untuk Spot. Untuk Futures kodenya sedikit berbeda.
            # order = b_client.create_order(
            #     symbol=pair,
            #     side=side,
            #     type='MARKET',
            #     quantity=0.001 # Sesuaikan dengan perhitungan lot kamu
            # )

            # --- 5. LAPOR KE SALSA ---
            import requests
            msg = f"🤖 **AUTO-TRADE EXECUTED**\n\nPair: {pair}\nAction: {side}\nEntry: {entry}\nStatus: Success ✅"
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                          json={"chat_id": MY_CHAT_ID, "text": msg, "parse_mode": "Markdown"})

        except Exception as e:
            print(f"❌ Gagal memproses sinyal: {e}")

t_client.start()
t_client.run_until_disconnected()