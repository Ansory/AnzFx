import streamlit as st
import requests

# --- KONFIGURASI BOT ---
# Masukkan data asli kamu di sini
TOKEN = "8348453058:AAHlGgxkPjLX_GwPuvUzXIsLqKzoMHEJAsM"
CHAT_ID = "913800755"

def kirim_telegram(pesan):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": pesan, "parse_mode": "Markdown"}
    try:
        response = requests.post(url, data=data)
        return response
    except Exception as e:
        return None

# --- TAMPILAN APLIKASI ---
st.set_page_config(page_title="AnzFx Controller", page_icon="🎮")
st.title("🎮 AnzFx Signal Controller")
st.write("Kirim perintah trading langsung ke Telegram")

with st.form("signal_form"):
    pair = st.text_input("🪙 Pair", value="XAUUSD").upper()
    side = st.selectbox("⚡ Side", ["BUY", "SELL"])
    
    order_type = st.radio("🛠️ Order Method", ["Order Now (Market)", "Order Limit"])
    
    # Input Entry Price
    entry = st.text_input("🎯 Entry Price", value="0")
        
    st.markdown("---")
    # Input TP 1, TP 2, dan SL
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

    # Menyusun pesan secara dinamis (Hanya baris yang diisi yang muncul)
    garis_pesan = [
        f"⚠️ **COMMAND: {status_text}** ⚠️",
        "",
        f"Symbol: {pair}",
        f"Action: {side}",
        f"Entry: {entry_final}",
        f"TP 1: {tp1}"
    ]
    
    # Tambahkan TP 2 hanya jika ada isinya
    if tp2.strip():
        garis_pesan.append(f"TP 2: {tp2}")
        
    garis_pesan.append(f"SL: {sl}")
    
    pesan_final = "\n".join(garis_pesan)
    
    # Proses Pengiriman
    res = kirim_telegram(pesan_final)
    
    if res and res.status_code == 200:
        st.success(f"🚀 Perintah {status_text} Berhasil Dikirim!")
        st.balloons()
    else:
        error_msg = res.text if res else "Koneksi Gagal"
        st.error(f"❌ Gagal! Pastikan Token/ID Benar. Detail: {error_msg}")