import streamlit as st
import requests

# --- KONFIGURASI BOT ---
# Pastikan Token dan Chat ID ini sudah benar
TOKEN = "8348453058:AAHlGgxkPjLX_GwPuvUzXIsLqKzoMHEJAsM"
CHAT_ID = "913800755"

def kirim_telegram(pesan):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": pesan, "parse_mode": "Markdown"}
    return requests.post(url, data=data)

# --- TAMPILAN APLIKASI ---
st.set_page_config(page_title="AnzFx Controller", page_icon="🎮", layout="centered")
st.title("🎮 AnzFx Signal Controller")

with st.form("signal_form"):
    pair = st.text_input("🪙 Pair", value="BTC/USDT").upper()
    side = st.selectbox("⚡ Side", ["BUY", "SELL"])
    
    order_type = st.radio("🛠️ Order Method", ["Order Now (Market)", "Order Limit"])
    
    col_entry, col_qty = st.columns(2)
    with col_entry:
        entry = st.text_input("🎯 Entry Price", value="0")
    with col_qty:
        qty = st.text_input("📦 Qty/Lot", value="0.01")
        
    # Input TP 1, TP 2, dan SL
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

    # Menyusun pesan secara dinamis
    garis_pesan = [
        f"⚠️ **COMMAND: {status_text}** ⚠️",
        "",
        f"Symbol: {pair}",
        f"Action: {side}",
        f"Entry: {entry_final}",
        f"Qty: {qty}",
        f"TP 1: {tp1}"
    ]
    
    # Hanya tambahkan TP 2 jika kotaknya diisi
    if tp2:
        garis_pesan.append(f"TP 2: {tp2}")
        
    garis_pesan.append(f"SL: {sl}")
    
    # Gabungkan menjadi satu string pesan
    pesan_final = "\n".join(garis_pesan)
    
    res = kirim_telegram(pesan_final)
    if res.status_code == 200:
        st.success(f"🚀 Perintah {status_text} Berhasil Dikirim!")
        if not tp2:
            st.info("Info: Dikirim dengan 1 Target Profit.")
        st.balloons()
    else:
        st.error(f"❌ Gagal! Periksa Token/Chat ID. Error: {res.text}")