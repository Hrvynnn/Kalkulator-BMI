import streamlit as st
import json
import random
import os
from google import genai

# ==========================================
# KONFIGURASI API GEMINI
# ==========================================

# Mengatur konfigurasi halaman
st.set_page_config(page_title="Kalkulator BMI", page_icon="⚖️", layout="centered")

# ==========================================
# FUNGSI AI
# FIX #1: Client dibuat di dalam fungsi agar st.cache_data bekerja dengan benar
# ==========================================
@st.cache_data(ttl=3600, show_spinner=False)
def dapatkan_evaluasi_ai(nama, bmi, kategori, umur, gender):
    prompt = f"""
    Berikan 1 paragraf evaluasi kesehatan (maksimal 4 kalimat) 
    untuk pasien bernama {nama} ({gender}, {umur} tahun) yang memiliki skor BMI {bmi:.1f} (Kategori: {kategori}). 
    Berikan kalimat yang ramah, berempati, dan memotivasi. 
    Langsung pada inti evaluasinya. Dilarang memberikan salam pembuka atau penutup.
    """
    try:
        # FIX #1: Inisialisasi client di dalam fungsi supaya cache aman
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
        response = _client.models.generate_content(model='gemini-flash-latest', contents=prompt)
        return response.text
    except Exception as e:
        return f"Gagal mengambil data evaluasi AI saat ini. (Error: {e})"

# ==========================================
# INJEKSI CUSTOM CSS (HIGH CONTRAST LAYLA THEME)
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Poppins', sans-serif !important; }
    .stApp { background-color: #292929; }
    label, label p, label div { color: #5C7CFA !important; font-weight: 600 !important; }
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important; border-radius: 12px !important;
        border: 2px solid #94A3B8 !important; box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    }
    input, div[data-baseweb="select"] * { color: #0F172A !important; font-weight: 500 !important; }
    .stButton>button {
        background-color: #5C7CFA !important; color: #FFFFFF !important;
        border-radius: 12px !important; border: none !important;
        padding: 12px 24px !important; font-weight: 600 !important; font-size: 16px !important;
        width: 100%; transition: all 0.3s ease; box-shadow: 0 4px 12px rgba(92, 124, 250, 0.4) !important;
        margin-top: 10px;
    }
    .stButton>button:hover { background-color: #4C6EF5 !important; transform: translateY(-2px); }
    .result-card {
        background-color: #FFFFFF; padding: 1px; border-radius: 16px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.08); margin-top: 25px; margin-bottom: 20px;
    }
    .stAlert { border-radius: 12px !important; border: 1px solid rgba(0,0,0,0.1) !important; }
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# FUNGSI SARAN MAKANAN LOKAL
# ==========================================
def load_food_data():
    file_path = 'saran_makanan.json'
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return None

food_data = load_food_data()

def tampilkan_saran_variatif(kategori_key):
    if not food_data:
        st.error("File saran_makanan.json tidak ditemukan!")
        return

    saran = food_data[kategori_key]
    st.markdown("### 🥗 Rekomendasi Makanan Anda")
    st.write("Berikut adalah saran makanan dari setiap kelompok nutrisi :")

    for kelompok, daftar_makanan in saran["makanan"].items():
        pilihan_acak = random.choice(daftar_makanan)
        st.markdown(f"- **{kelompok}**: {pilihan_acak}")

    st.markdown("---")
    st.markdown("### 💡 Tips Kesehatan")
    for tip in saran["tips"]:
        st.info(tip)

# ==========================================
# HEADER APLIKASI
# ==========================================
st.markdown("""
<div style="text-align: center; margin-bottom: 30px; margin-top: -30px;">
    <h1 style="color: #5C7CFA; font-weight: 700; margin-bottom: 0;">Kalkulator BMI</h1>
    <p style="color: #e0e0e0; font-weight: 500;">Count Your Body Mass Index</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# INPUT PENGGUNA (LIVE DATA)
# ==========================================
nama_input = st.text_input("Nama (Opsional, untuk laporan)", placeholder="Masukkan nama Anda")

col_gender, col_umur = st.columns(2)
with col_gender:
    gender = st.selectbox("Pilih Gender", ["Laki-laki", "Perempuan"])
with col_umur:
    umur = st.number_input("Umur (tahun)", min_value=2, max_value=120, value=25, step=1)

col_berat, col_tinggi = st.columns(2)
with col_berat:
    berat_badan = st.number_input("Berat Badan (kg)", min_value=1.0, value=60.0, step=0.1, format="%.1f")
with col_tinggi:
    tinggi_badan_cm = st.number_input("Tinggi Badan (cm)", min_value=1.0, value=165.0, step=0.1, format="%.1f")

# ==========================================
# LOGIKA PENYIMPANAN STATE & PERHITUNGAN
# ==========================================
if 'hitung_clicked' not in st.session_state:
    st.session_state.hitung_clicked = False

if st.button("Hitung Sekarang", type="primary"):
    tinggi_badan_m = tinggi_badan_cm / 100
    bmi = berat_badan / (tinggi_badan_m ** 2)

    # FIX #2: Kategori obesitas sekarang punya key "obese" tersendiri
    if bmi < 18.5:
        kategori_teks = "Kekurangan berat badan (Underweight)"
        kategori_json = "underweight"
        bar_color = "#3B82F6"
    elif 18.5 <= bmi <= 24.9:
        kategori_teks = "Berat badan ideal (Normal)"
        kategori_json = "normal"
        bar_color = "#22C55E"
    elif 25.0 <= bmi <= 29.9:
        kategori_teks = "Kelebihan berat badan (Overweight)"
        kategori_json = "overweight"
        bar_color = "#EAB308"
    else:
        kategori_teks = "Obesitas (Obese)"
        kategori_json = "obese"   # FIX #2: Pisahkan key obese dari overweight
        bar_color = "#EF4444"

    st.session_state.update({
        'hitung_clicked': True,
        'bmi': bmi,
        'kategori_teks': kategori_teks,
        'kategori_json': kategori_json,
        'bar_color': bar_color,
        'nama': nama_input if nama_input else "Pengguna",
        'gender': gender,
        'umur': umur
    })

# ==========================================
# MENAMPILKAN HASIL DARI STATE
# ==========================================
if st.session_state.hitung_clicked:
    bmi = st.session_state.bmi

    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: #5C7CFA; margin-bottom: 5px;'>Skor BMI Anda: <span style='color: #3B5BDB; font-size: 1.5em; font-weight: 700;'>{bmi:.2f}</span></h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #475569; font-size: 0.9em; margin-bottom: 20px; font-weight: 500;'>Profil: {st.session_state.gender}, {st.session_state.umur} Tahun</p>", unsafe_allow_html=True)

    # Progress Bar
    max_bmi_visual = 50.0
    progress_percentage = min((bmi / max_bmi_visual) * 100, 100)
    custom_bar_html = f"""
    <div style="width: 100%; background-color: #E2E8F0; border-radius: 12px; margin: 10px 0 20px 0; box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);">
        <div style="width: {progress_percentage}%; background-color: {st.session_state.bar_color}; height: 16px; border-radius: 12px; transition: all 0.5s ease-in-out;"></div>
    </div>
    """
    st.markdown(custom_bar_html, unsafe_allow_html=True)

    # FIX #3: Pengecekan kategori pakai kategori_json yang konsisten, bukan string panjang
    if st.session_state.kategori_json == "underweight":
        st.warning(f"📉 Kategori: **{st.session_state.kategori_teks}**")
    elif st.session_state.kategori_json == "normal":
        st.success(f"✅ Kategori: **{st.session_state.kategori_teks}**")
    elif st.session_state.kategori_json == "overweight":
        st.warning(f"📈 Kategori: **{st.session_state.kategori_teks}**")
    else:  # obese
        st.error(f"🚨 Kategori: **{st.session_state.kategori_teks}**")

    # Tampilkan saran makanan lokal
    tampilkan_saran_variatif(st.session_state.kategori_json)

    st.markdown("---")

    # ==========================================
    # TOMBOL LAPORAN AI
    # ==========================================
    if st.button("✨ Analisis AI", use_container_width=True):
        with st.spinner("AI sedang merangkum evaluasi kesehatan Anda..."):
            evaluasi = dapatkan_evaluasi_ai(
                st.session_state.nama,
                st.session_state.bmi,
                st.session_state.kategori_teks,
                st.session_state.umur,
                st.session_state.gender
            )
            # FIX #4: Pisahkan HTML dan Markdown, tidak dicampur dalam satu st.markdown
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### Hasil Analisis AI")
            st.info(evaluasi)

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 0.8em; color: #e0e0e0; font-weight: 500;'>Perhitungan didasarkan pada rumus standar WHO.</p>", unsafe_allow_html=True)
