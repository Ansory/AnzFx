import streamlit as st
import requests

# --- DATA BOT TELEGRAM ---
# Masukkan Token dari @BotFather dan ID dari @userinfobot
TOKEN = "8348453058:AAHlGgxkPjLX_GwPuvUzXIsLqKzoMHEJAsM"
CHAT_ID = "913800755"

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    return requests.post(url, data=payload)

# --- TAMPILAN DASHBOARD ---
st.set_page_config(page_title="AnzFx Signal", page_icon="📈")
st.title("📈 AnzFx Signal Center")

with st.form("my_form"):
    st.write("Isi detail sinyal di bawah:")
    pair = st.text_input("🪙 Pair", value="BTC/USDT")
    action = st.selectbox("⚡ Action", ["BUY", "SELL"])
    entry = st.text_input("🎯 Entry Price")
    tp = st.text_input("💰 Take Profit")
    sl = st.text_input("🛑 Stop Loss")
    
    submitted = st.form_submit_button("KIRIM KE TELEGRAM")

if submitted:
    icon = "🟢" if action == "BUY" else "🔴"
    pesan = (
        f"{icon} **ANZ FX SIGNAL: {action}** {icon}\n\n"
        f"💎 **Pair:** `{pair.upper()}`\n"
        f"📥 **Entry:** `{entry}`\n"
        f"🎯 **TP:** `{tp}`\n"
        f"🛑 **SL:** `{sl}`"
    )
    
    response = send_to_telegram(pesan)
    if response.status_code == 200:
        st.success("Sinyal berhasil dikirim!")
        st.balloons()
    else:
        st.error(f"Gagal kirim! Error: {response.text}")