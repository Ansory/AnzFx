import streamlit as st
import requests

# --- KONFIGURASI BOT ---
TOKEN = "8348453058:AAHlGgxkPjLX_GwPuvUzXlsLqKzoMHEJAsM"
CHAT_ID = "913800755"

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

    # Susun Pesan
    pesan = (
        f"⚠️ **COMMAND: {status_text}** ⚠️\n\n"
        f"Symbol: {pair}\n"
        f"Action: {side}\n"
        f"Entry: {entry_final}\n"
        f"TP 1: {tp1}\n"
    )
    if tp2.strip():
        pesan += f"TP 2: {tp2}\n"
    pesan += f"SL: {sl}"

    # Kirim ke Telegram
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": pesan, "parse_mode": "Markdown"}
    
    try:
        res = requests.post(url, json=payload)
        if res.status_code == 200:
            st.success("🚀 Berhasil Dikirim ke Telegram Salsa!")
            st.balloons()
        else:
            st.error(f"❌ Telegram Menolak: {res.text}")
    except Exception as e:
        st.error(f"❌ Masalah Koneksi: {e}")