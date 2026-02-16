import streamlit as st
import requests

# --- KONFIGURASI BOT ---
TOKEN = "8348453058:AAHlGgxkPjLX_GwPuvUzXlsLqKzoMHEJAsM"
CHAT_ID = "913800755"

def kirim_telegram(pesan):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": pesan, "parse_mode": "Markdown"}
    try:
        # Mengirim data ke Telegram
        response = requests.post(url, data=data)
        return response
    except Exception as e:
        return None

# --- TAMPILAN APLIKASI ---
st.set_page_config(page_title="AnzFx Controller", page_icon="🎮")
st.title("🎮 AnzFx Signal Controller")

with st.form("signal_form"):
    pair = st.text_input("🪙 Pair", value="XAUUSD").upper()
    side = st.selectbox("⚡ Side", ["BUY", "SELL"])
    order_type = st.radio("🛠️ Order Method", ["Order Now (Market)", "Order Limit"])
    entry = st.text_input("🎯 Entry Price", value="0")
    
    st.markdown("---")
    col_tp1, col_tp2 = st.columns(2)
    with col_tp1:
        tp1 = st.text_input("💰 Take Profit 1")
    with col_tp2:
        tp2 = st.text_input("💰 Take Profit 2 (Opsional)")
        
    sl = st.text_input("🛑 Stop Loss")
    
    submit = st.form_submit_button("KIRIM PERINTAH SEKARANG")

if submit:
    status_text = "MARKET_ORDER" if order_type == "Order Now (Market)" else "LIMIT_ORDER"
    entry_final = "NOW" if order_type == "Order Now (Market)" else entry

    # Menyusun pesan
    garis_pesan = [
        f"⚠️ **COMMAND: {status_text}** ⚠️",
        "",
        f"Symbol: {pair}",
        f"Action: {side}",
        f"Entry: {entry_final}",
        f"TP 1: {tp1}"
    ]
    
    if tp2.strip():
        garis_pesan.append(f"TP 2: {tp2}")
        
    garis_pesan.append(f"SL: {sl}")
    pesan_final = "\n".join(garis_pesan)
    
    # Eksekusi fungsi kirim
    res = kirim_telegram(pesan_final)
    
    if res and res.status_code == 200:
        st.success(f"🚀 Perintah {status_text} Berhasil Dikirim!")
        st.balloons()
    else:
        st.error("❌ Gagal mengirim! Pastikan bot sudah di-START di Telegram.")