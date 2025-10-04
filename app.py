

import streamlit as st
import google.generativeai as genai
from exa_py import Exa
import sqlite3
import pandas as pd
from datetime import datetime
import uuid
import textwrap


DB_NAME = "learning_tracker.db"

def init_db():
    """Inisialisasi database dan tabel jika belum ada."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS learning_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            user_query TEXT NOT NULL,
            search_results TEXT,
            llm_response TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_to_db(session_id, query, search_data, response):
    """Menyimpan riwayat percakapan ke database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO learning_history (session_id, timestamp, user_query, search_results, llm_response) VALUES (?, ?, ?, ?, ?)",
        (session_id, timestamp, query, str(search_data), response)
    )
    conn.commit()
    conn.close()

def view_learning_data():
    """Mengambil dan menampilkan data dari database."""
    conn = sqlite3.connect(DB_NAME)
    try:
        df = pd.read_sql_query("SELECT * FROM learning_history", conn)
        st.dataframe(df)
    except Exception as e:
        st.warning(f"Belum ada data pembelajaran untuk ditampilkan. Error: {e}")
    finally:
        conn.close()


def get_all_sessions():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT session_id, MIN(timestamp) FROM learning_history GROUP BY session_id ORDER BY MIN(timestamp) DESC")
    sessions = cursor.fetchall()
    conn.close()
    return sessions

def get_session_messages(session_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT user_query, llm_response, timestamp FROM learning_history WHERE session_id=? ORDER BY timestamp ASC", (session_id,))
    messages = cursor.fetchall()
    conn.close()
    return messages

def delete_session(session_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM learning_history WHERE session_id=?", (session_id,))
    conn.commit()
    conn.close()

def delete_all_sessions():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM learning_history")
    conn.commit()
    conn.close()

def get_session_titles():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT session_id, MIN(timestamp), SUBSTR(MIN(user_query), 1, 80)
        FROM learning_history
        GROUP BY session_id
        ORDER BY MIN(timestamp) DESC
    """)
    sessions = cursor.fetchall()
    conn.close()
  
    return sessions


st.sidebar.header("⚙️ Konfigurasi API")

if 'gemini_api_key' not in st.session_state:
    st.session_state.gemini_api_key = ""
if 'exa_api_key' not in st.session_state:
    st.session_state.exa_api_key = ""

gemini_key_input = st.sidebar.text_input(
    "🔑 Gemini API Key", type="password", value=st.session_state.gemini_api_key,
    placeholder="Masukkan kunci API Gemini Anda"
)
exa_key_input = st.sidebar.text_input(
    "🔑 Exa API Key", type="password", value=st.session_state.exa_api_key,
    placeholder="Masukkan kunci API Exa Anda"
)

if st.sidebar.button("Simpan Konfigurasi"):
    st.session_state.gemini_api_key = gemini_key_input
    st.session_state.exa_api_key = exa_key_input
    st.sidebar.success("API Keys berhasil disimpan untuk sesi ini!")
    st.rerun()


st.title("📚 Chatbot Pembelajaran Cerdas")
st.caption("Didukung oleh Gemini & Exa Search")


current_date_for_display = datetime.now().strftime('%d %B %Y')
st.info(f"🗓️ **Konteks Waktu:** Informasi disesuaikan dengan tanggal hari ini: **{current_date_for_display}**")

init_db()


if st.session_state.gemini_api_key:
    try:
        genai.configure(api_key=st.session_state.gemini_api_key)
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        exa = None
        if st.session_state.exa_api_key:
            try:
                exa = Exa(api_key=st.session_state.exa_api_key)
            except Exception as e:
                st.warning(f"API Exa gagal dikonfigurasi: {e}. Chatbot tetap berjalan tanpa Exa.")

        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "session_id" not in st.session_state:
            st.session_state.session_id = str(uuid.uuid4())

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Tanyakan sesuatu..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                current_date_str = datetime.now().strftime("%d %B %Y")
                search_context = ""
                search_results_str = "Pencarian tidak dilakukan atau gagal."
                if exa:
                    with st.spinner("Mencari informasi terbaru dengan Exa..."):
                        try:
                            search_query = f"Berdasarkan informasi terbaru hingga {current_date_str}, {prompt}"
                            search_response = exa.search_and_contents(
                                search_query,
                                num_results=3,  
                                highlights={}
                            )
                            highlights_list = []
                            for item in search_response.results:
                                if item.highlights:
                                    highlights_list.extend(item.highlights)
                            search_context = "\n".join(highlights_list)
                            search_results_str = str(search_response.results)
                            st.info("✅ Pencarian informasi real-time berhasil.")
                        except Exception as e:
                            st.warning(f"⚠️ Gagal melakukan pencarian dengan Exa: {e}. Gemini akan menjawab tanpa konteks tambahan.")
                else:
                    st.info("🔎 Exa tidak tersedia. Jawaban hanya dari Gemini.")

                with st.spinner("Gemini sedang menganalisis..."):
                    enhanced_prompt = f"""
                    Anda adalah asisten AI yang cerdas dan selalu memberikan informasi terbaru.
                    Konteks Waktu Penting: Tanggal hari ini adalah {current_date_str}.

                    Berdasarkan cuplikan informasi berikut dari pencarian web:
                    ---
                    {search_context}
                    ---
                    Dengan mempertimbangkan bahwa hari ini adalah {current_date_str}, jawab pertanyaan pengguna berikut: "{prompt}"

                    Pastikan jawaban Anda relevan, akurat sesuai waktu saat ini, dan disajikan dalam Bahasa Indonesia.
                    """
                    try:
                        response = model.generate_content(enhanced_prompt)
                        full_response = response.text
                    except Exception as e:
                        full_response = f"❌ Maaf, terjadi kesalahan saat menghubungi Gemini API: {e}"

                st.markdown(full_response)

           
            if exa and search_context:
                with st.expander("🔍 Lihat hasil pencarian Exa"):
                    st.write(search_context)

            st.session_state.messages.append({"role": "assistant", "content": full_response})
            save_to_db(st.session_state.session_id, prompt, search_results_str, full_response)

    except Exception as e:
        st.error(f"Terjadi kesalahan konfigurasi API Gemini. Pastikan API Key yang Anda masukkan benar. Detail: {e}")

else:
    st.info("👋 Selamat datang! Masukkan API Key Gemini Anda di sidebar untuk memulai percakapan.")