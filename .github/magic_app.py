import streamlit as st
import requests
import re

# --- KONFIGURASI BOT ---
TOKEN = "8348453058:AAEdjA6d9YQSo1qriElIm5Ll9lD0m7N_h-0"
CHAT_ID = "913800755"

def kirim_telegram(pesan):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        res = requests.post(url, json={"chat_id": CHAT_ID, "text": pesan, "parse_mode": "Markdown"})
        return res
    except:
        return None

# --- TAMPILAN APLIKASI ---
st.set_page_config(page_title="AnzFx Magic Detector", page_icon="🪄")
st.title("🪄 AnzFx Magic Signal Detector")
st.write("Tempel teks analisa kamu di bawah, sistem akan otomatis mendeteksi sinyalnya.")

# Input Area untuk Paste Teks
raw_text = st.text_area("Paste Analisa Di Sini:", height=300, placeholder="Halo Tuan Ansory, 📊 XAUUSD...")

if st.button("DETEKSI & KIRIM SINYAL"):
    if raw_text:
        try:
            # --- PROSES DETEKSI (REGEX) ---
            # Mencari Pair (Contoh: XAUUSD)
            pair = re.search(r"📊\s*(\w+)", raw_text)
            pair = pair.group(1) if pair else "UNKNOWN"

            # Mencari Side (BUY/SELL)
            side = "BUY" if "BUY" in raw_text.upper() else "SELL" if "SELL" in raw_text.upper() else "ORDER"

            # Mencari Entry
            entry = re.search(r"Entry:\s*([\d.]+)", raw_text)
            entry = entry.group(1) if entry else "NOW"

            # Mencari SL
            sl = re.search(r"Stop Loss:\s*([\d.]+)", raw_text)
            sl = sl.group(1) if sl else "-"

            # Mencari TP1 & TP2
            tp1 = re.search(r"Target 1:\s*([\d.]+)", raw_text)
            tp1 = tp1.group(1) if tp1 else "-"
            
            tp2 = re.search(r"Target 2:\s*([\d.]+)", raw_text)
            tp2 = tp2.group(1) if tp2 else None

            # --- MENYUSUN PESAN UNTUK TELEGRAM ---
            pesan_final = (
                f"🚀 **NEW SIGNAL DETECTED** 🚀\n\n"
                f"🪙 Symbol: {pair}\n"
                f"⚡ Action: {side}\n"
                f"🎯 Entry: {entry}\n"
                f"💰 TP 1: {tp1}\n"
            )
            if tp2:
                pesan_final += f"💰 TP 2: {tp2}\n"
            
            pesan_final += f"🛑 SL: {sl}\n\n"
            pesan_final += "✅ *Detected by AnzFx Magic System*"

            # --- KIRIM ---
            response = kirim_telegram(pesan_final)
            if response and response.status_code == 200:
                st.success("✅ Sinyal Berhasil Dideteksi & Terkirim!")
                st.balloons()
                st.markdown("### Hasil Deteksi:")
                st.code(pesan_final)
            else:
                st.error("❌ Gagal mengirim. Cek Token atau Koneksi.")
                
        except Exception as e:
            st.error(f"❌ Gagal membaca format teks: {e}")
    else:
        st.warning("⚠️ Silakan tempel teks analisa dulu!")