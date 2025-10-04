**Chatbot Pembelajaran Cerdas (Intelligent Learning Chatbot)**

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)

Selamat datang di Chatbot Pembelajaran Cerdas! Aplikasi ini adalah asisten AI interaktif yang dibangun menggunakan Streamlit, ditenagai oleh model bahasa canggih dari Google Gemini dan diperkaya dengan kemampuan pencarian web real-time dari Exa AI.

Aplikasi ini dirancang untuk memberikan jawaban yang tidak hanya cerdas tetapi juga relevan dengan waktu saat ini, menjadikannya alat yang fleksibel untuk belajar dan mencari informasi terbaru.

## ✨ Fitur Utama

-   **Antarmuka Interaktif**: Dibuat dengan Streamlit untuk pengalaman pengguna yang ramah dan responsif.
-   **Kecerdasan Kontekstual**: Ditenagai oleh model **Gemini 2.5 Flash**, mampu memahami dan merespons percakapan dalam bahasa alami.
-   **Informasi Real-time**: Terintegrasi secara opsional dengan **Exa Search API** untuk mengambil data terbaru dari internet, memastikan jawaban selalu up-to-date.
-   **Sadar Waktu**: Secara otomatis menyertakan tanggal hari ini sebagai konteks, sehingga relevan untuk pertanyaan tentang peristiwa terkini.
-   **Riwayat Percakapan**: Semua interaksi disimpan secara lokal dalam database SQLite (`learning_tracker.db`) untuk referensi di masa mendatang.
-   **Konfigurasi Mudah**: Masukkan API key langsung di antarmuka aplikasi, tidak perlu mengelola file `.env`.

## 🚀 Cara Kerja

Aplikasi ini mengintegrasikan beberapa teknologi kunci:
1.  **Frontend (UI)**: **Streamlit** menyediakan semua komponen antarmuka, mulai dari area chat hingga sidebar konfigurasi.
2.  **Otak (LLM)**: **Google Gemini** berfungsi sebagai model bahasa utama yang memproses pertanyaan, memahami konteks, dan menghasilkan jawaban.
3.  **Pencarian Web**: **Exa AI** bertindak sebagai "pencari fakta" yang menjelajahi web untuk menemukan cuplikan informasi relevan terkait pertanyaan pengguna. Informasi ini kemudian diberikan kepada Gemini sebagai konteks tambahan.
4.  **Penyimpanan**: **SQLite** digunakan sebagai database file yang ringan untuk menyimpan setiap sesi percakapan.

## 🛠️ Instalasi dan Pengaturan

Ikuti langkah-langkah ini untuk menjalankan aplikasi di komputer lokal Anda.

### 1. Prasyarat
-   [Python](https://www.python.org/downloads/) (versi 3.8 atau lebih baru)
-   `pip` (package installer untuk Python)

### 2. Dapatkan Kode
Unduh atau clone repositori ini ke komputer Anda.

### 3. Instal Dependensi
Buka terminal atau command prompt, navigasikan ke direktori proyek, dan jalankan perintah berikut untuk menginstal semua library yang diperlukan:
```bash
pip install -r requirements.txt
```

## ▶️ Menjalankan Aplikasi

Setelah instalasi selesai, jalankan aplikasi dengan perintah berikut di terminal Anda:
```bash
streamlit run app.py
```
Aplikasi akan secara otomatis terbuka di browser default Anda.

##  kullanım kılavuzu (Cara Menggunakan)

1.  **Buka Aplikasi**: Setelah menjalankan perintah di atas, sebuah tab browser akan terbuka dengan alamat seperti `http://localhost:8501`.
2.  **Konfigurasi API**:
    -   Di **sidebar** sebelah kiri, Anda akan melihat bagian "Konfigurasi API".
    -   **Wajib**: Masukkan **Gemini API Key** Anda. Aplikasi tidak akan berjalan tanpanya.
    -   **Opsional**: Masukkan **Exa API Key** Anda untuk mengaktifkan fitur pencarian web. Jika dibiarkan kosong, chatbot akan tetap berfungsi tetapi hanya mengandalkan pengetahuan internal Gemini.
    -   Klik tombol **"Simpan Konfigurasi"**.
3.  **Mulai Chat**: Setelah API key disimpan, antarmuka chat utama akan siap digunakan. Ketik pertanyaan Anda di kotak input di bagian bawah dan tekan Enter.

## 🔑 Mendapatkan API Keys
-   **Google Gemini API Key**: Dapatkan kunci Anda secara gratis di [Google AI Studio](https://aistudio.google.com/app/apikey).
-   **Exa API Key**: Daftar dan dapatkan kunci gratis Anda di [website Exa AI](https://exa.ai/).

## 📁 Struktur File Proyek

```
.
├── app.py                 # Skrip utama aplikasi Streamlit
├── db_learn.py            # Utilitas untuk manajemen database (tidak digunakan langsung oleh app.py)
├── requirements.txt       # Daftar pustaka Python yang dibutuhkan
└── learning_tracker.db    # File database SQLite (dibuat otomatis saat aplikasi dijalankan pertama kali)
```

---


**⭐️ Jika Anda merasa konten ini bermanfaat, jangan lupa memberi repositori tersebut bintang.**
