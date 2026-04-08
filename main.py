import streamlit as st

# Mengatur konfigurasi halaman
st.set_page_config(page_title="Kalkulator BMI", page_icon="⚖️", layout="centered")

# ==========================================
# INJEKSI CUSTOM CSS (HIGH CONTRAST LAYLA THEME)
# ==========================================
st.markdown("""
<style>
    /* Mengimpor font Poppins dari Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

    /* Menerapkan font dasar */
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif !important;
    }

    /* Mengubah warna latar belakang utama (Soft Blue-Grey yang lebih solid) */
    .stApp {
        background-color: #292929; 
    }

    /* Memaksa warna teks Label (Pilih Gender, Umur, dll) menjadi gelap kontras */
    label, label p, label div {
        color: #5C7CFA !important; /* Warna biru dongker kehitaman (Sangat gelap) */
        font-weight: 600 !important;
    }

    /* Modifikasi kotak input (Number input & Selectbox) */
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important; /* Background input putih bersih */
        border-radius: 12px !important;
        border: 2px solid #94A3B8 !important; /* Border abu-abu kebiruan yang lebih jelas */
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    }

    /* Memaksa teks di DALAM kotak input agar kontras (Hitam/Gelap) */
    input, div[data-baseweb="select"] * {
        color: #0F172A !important;
        -webkit-text-fill-color: #0F172A !important;
        font-weight: 500 !important;
    }

    /* Modifikasi Tombol Hitung */
    .stButton>button {
        background-color: #5C7CFA !important; /* Biru cerah kontras */
        color: #FFFFFF !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(92, 124, 250, 0.4) !important;
        margin-top: 10px;
        
    }
    .stButton>button:hover {
        background-color: #4C6EF5 !important; /* Biru sedikit lebih gelap saat hover */
        transform: translateY(-2px);
    }

    /* Membuat kontainer hasil agar terlihat seperti 'Card' putih dengan bayangan tegas */
    .result-card {
        background-color: #FFFFFF;
        padding: 2px;
        border-radius: 16px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
        margin-top: 25px;
        margin-bottom: 20px;
    }

    /* Teks dalam card */
    .result-text {
        color: #1E293B !important;
    }

    /* Modifikasi Kotak Peringatan (Alerts) */
    .stAlert {
        border-radius: 12px !important;
        border: 1px solid rgba(0,0,0,0.1) !important;
    }

    /* Menyembunyikan elemen header default Streamlit */
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

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
# INPUT PENGGUNA
# ==========================================
# Input Gender dan Umur
col_gender, col_umur = st.columns(2)
with col_gender:
    gender = st.selectbox("Pilih Gender", ["Laki-laki", "Perempuan"])
with col_umur:
    umur = st.number_input("Umur (tahun)", min_value=2, max_value=120, value=25, step=1)

st.markdown("<br>", unsafe_allow_html=True)

# Input Berat dan Tinggi
col_berat, col_tinggi = st.columns(2)
with col_berat:
    berat_badan = st.number_input("Berat Badan (kg)", min_value=1.0, value=60.0, step=0.1, format="%.1f")
with col_tinggi:
    tinggi_badan_cm = st.number_input("Tinggi Badan (cm)", min_value=1.0, value=165.0, step=0.1, format="%.1f")

# ==========================================
# TOMBOL HITUNG DAN LOGIKA
# ==========================================
if st.button("Hitung Sekarang", type="primary"):
    tinggi_badan_m = tinggi_badan_cm / 100
    bmi = berat_badan / (tinggi_badan_m ** 2)
    
    # Membungkus hasil dalam "Card"
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    
    st.markdown(f"<h3 style='text-align: center; color: #5C7CFA; margin-bottom: 5px;'>Skor BMI Anda: <span style='color: #3B5BDB; font-size: 1.5em; font-weight: 700;'>{bmi:.2f}</span></h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #e0e0e0; font-size: 0.9em; margin-bottom: 20px; font-weight: 500;'>Profil: {gender}, {umur} Tahun</p>", unsafe_allow_html=True)
    
    # ==========================================
    # PROGRESS BAR DINAMIS DIMULAI DI SINI
    # ==========================================
    # Menentukan warna berdasarkan nilai BMI
    if bmi < 18.5:
        bar_color = "#3B82F6"  # Biru (Underweight)
    elif 18.5 <= bmi <= 24.9:
        bar_color = "#22C55E"  # Hijau (Normal)
    elif 25.0 <= bmi <= 29.9:
        bar_color = "#EAB308"  # Kuning (Overweight)
    else:
        bar_color = "#EF4444"  # Merah (Obese)

    # Kalkulasi persentase lebar bar (Maksimum visual BMI di 50 agar proporsional)
    max_bmi_visual = 50.0
    progress_percentage = min((bmi / max_bmi_visual) * 100, 100)

    # Render custom HTML untuk progress bar
    custom_bar_html = f"""
    <div style="width: 100%; background-color: #333333; border-radius: 12px; margin: 10px 0 20px 0; box-shadow: inset 0 1px 3px rgba(0,0,0,0.2);">
        <div style="width: {progress_percentage}%; background-color: {bar_color}; height: 16px; border-radius: 12px; transition: all 0.5s ease-in-out;"></div>
    </div>
    """
    st.markdown(custom_bar_html, unsafe_allow_html=True)
    # ==========================================
    # PROGRESS BAR DINAMIS BERAKHIR DI SINI
    # ==========================================

    # Menentukan kategori dan menampilkan pesan
    if bmi < 18.5:
        st.warning("📉 Kategori: **Kekurangan berat badan (Underweight)**")
        st.info("Saran: Tambah asupan nutrisi dan kalori. Konsultasikan dengan ahli gizi.")
    elif 18.5 <= bmi <= 24.9:
        st.success("✅ Kategori: **Berat badan ideal (Normal)**")
        st.info("Saran: Luar biasa! Pertahankan gaya hidup sehat Anda dengan pola makan bergizi dan olahraga teratur.")
    elif 25.0 <= bmi <= 29.9:
        st.warning("📈 Kategori: **Kelebihan berat badan (Overweight)**")
        st.info("Saran: Mulailah perhatikan pola makan dan tingkatkan aktivitas fisik harian Anda.")
    else:
        st.error("🚨 Kategori: **Obesitas (Obese)**")
        st.info("Saran: Sangat disarankan untuk berkonsultasi dengan dokter atau ahli gizi untuk program penurunan berat badan.")
    
    # Menutup tag Card
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 0.8em; color: #e0e0e0; font-weight: 500;'>Perhitungan didasarkan pada rumus standar WHO.</p>", unsafe_allow_html=True)
