import streamlit as st
import requests

# --- 1. PENGATURAN BOT ---
# Pastikan Anda sudah 'Revoke Token' di BotFather untuk mendapatkan Token baru yang segar
TOKEN = "8348453058:AAEdjA6d9YQSo1qriElIm5Ll9lD0m7N_h-0"
CHAT_ID = "913800755"

# --- 2. TAMPILAN WEB ---
st.set_page_config(page_title="AnzFx Signal", page_icon="📈")
st.title("🚀 AnzFx Signal Center")

# Form Input
with st.form("main_form"):
    pair = st.text_input("🪙 Pair", value="XAUUSD").upper()
    side = st.selectbox("⚡ Side", ["BUY", "SELL"])
    order = st.radio("🛠️ Type", ["Market Order", "Limit Order"])
    entry = st.text_input("🎯 Entry Price", value="0")
    
    col1, col2 = st.columns(2)
    tp1 = col1.text_input("💰 TP 1")
    tp2 = col2.text_input("💰 TP 2 (Opsional)")
    
    sl = st.text_input("🛑 Stop Loss")
    
    tombol = st.form_submit_button("KIRIM SINYAL")

# --- 3. LOGIKA PENGIRIMAN ---
if tombol:
    # Susun teks pesan
    txt = f"⚠️ **{order.upper()}** ⚠️\n\n"
    txt += f"Symbol: {pair}\nAction: {side}\nEntry: {entry}\n"
    txt += f"TP 1: {tp1}\n"
    if tp2.strip():
        txt += f"TP 2: {tp2}\n"
    txt += f"SL: {sl}"

    # Kirim ke API Telegram
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        r = requests.post(url, json={"chat_id": CHAT_ID, "text": txt, "parse_mode": "Markdown"})
        if r.status_code == 200:
            st.success("✅ SINYAL TERKIRIM!")
            st.balloons()
        else:
            # Menampilkan pesan error asli dari Telegram
            st.error(f"❌ Gagal! Respons Telegram: {r.text}")
    except Exception as e:
        st.error(f"❌ Error Koneksi: {e}")