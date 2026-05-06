import streamlit as st
import json
import os

# ==========================================
# INJEKSI CUSTOM CSS (MENYAMAKAN TEMA DARI main.py)
# ==========================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
    
    /* FIX: Terapkan Poppins hanya pada elemen teks, JANGAN pakai [class*="css"] */
    html, body, h1, h2, h3, h4, h5, h6, p, li, td, th, label { 
        font-family: 'Poppins', sans-serif !important; 
    }
    
    /* Kembalikan font bawaan untuk icon Streamlit agar tidak jadi teks */
    span[data-testid="stIconMaterial"], .material-icons {
        font-family: 'Material Symbols Rounded', sans-serif !important;
    }

    .stApp { background-color: #292929; }
    h1, h2, h3, h4, h5, label { color: #5C7CFA !important; font-weight: 600 !important; }
    p, li, td, th { color: #e0e0e0 !important; }
    
    /* Styling khusus untuk expander (dropdown) */
    div[data-testid="stExpander"] {
        background-color: #3B3B3B !important; 
        border: 1px solid #5C7CFA !important;
        border-radius: 12px !important;
        margin-bottom: 15px;
        overflow: hidden;
    }
    div[data-testid="stExpander"] details summary { 
        background-color: #3B3B3B !important; 
        padding: 10px !important;
    }
    div[data-testid="stExpander"] details summary p {
        color: #5C7CFA !important;
        font-weight: 600 !important;
        font-size: 1.1em !important;
    }
    div[data-testid="stExpander"] details summary span[data-testid="stIconMaterial"] {
        color: #5C7CFA !important; /* Mewarnai icon panah */
    }

    /* Button Styling */
    .stButton>button, a[data-testid="stPageLink"] {
        background-color: #5C7CFA !important; color: #FFFFFF !important;
        border-radius: 12px !important; border: none !important;
        padding: 12px 24px !important; font-weight: 600 !important; font-size: 16px !important;
        width: 100%; transition: all 0.3s ease; box-shadow: 0 4px 12px rgba(92, 124, 250, 0.4) !important;
        margin-top: 10px; text-decoration: none; display: inline-block; text-align: center;
    }
    .stButton>button:hover, a[data-testid="stPageLink"]:hover { 
        background-color: #4C6EF5 !important; transform: translateY(-2px); 
    }
    
    /* Styling Card/Kotak */
    .info-card {
        background-color: #3B3B3B; padding: 20px; border-radius: 16px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.2); margin-top: 15px; margin-bottom: 20px;
        border-left: 5px solid #5C7CFA;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# FUNGSI LOAD DATA JSON
# ==========================================
def load_latihan_data():
    file_path = 'saran_latihan.json' # Pastikan file ini ada di root folder
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

# ==========================================
# HEADER HALAMAN
# ==========================================
st.markdown("""
<div style="text-align: center; margin-bottom: 30px; margin-top: -30px;">
    <h1 style="color: #5C7CFA; font-weight: 700; margin-bottom: 0;">Panduan Latihan Fisik</h1>
    <p style="color: #e0e0e0; font-weight: 500;">Rekomendasi Berdasarkan Evaluasi BMI Anda</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# LOGIKA UTAMA (CEK BMI & TAMPILKAN)
# ==========================================
if 'hitung_clicked' not in st.session_state or not st.session_state.hitung_clicked:
    # Jika pengguna belum menghitung BMI di halaman utama
    st.warning("⚠️ Silahkan hitung BMI Anda terlebih dahulu di halaman utama untuk mendapatkan rekomendasi yang sesuai.")
    st.page_link("beranda.py", label="Kembali ke Kalkulator BMI", icon="⬅️")

else:
    data_latihan = load_latihan_data()
    
    if not data_latihan:
        st.error("File 'saran_latihan.json' tidak ditemukan di direktori! Pastikan file berada pada lokasi yang benar.")
    else:
        # Mapping BMI kategori ke ID di JSON
        kategori_bmi = st.session_state.kategori_json
        
        # Logika pemetaan sesuai standar ilmu keolahragaan dari dokumen
        if kategori_bmi == "underweight":
            target_id = "hipertrofi"
        elif kategori_bmi == "normal":
            target_id = "weight_maintenance"
        else: # overweight & obese
            target_id = "fat_loss"

        # Mencari program yang cocok di list panduan_latihan
        program_pilihan = next((item for item in data_latihan["panduan_latihan"] if item["id"] == target_id), None)
        tips_umum = data_latihan.get("tips_umum", {})

        if program_pilihan:
            # 1. TAMPILKAN INFO UTAMA & DESKRIPSI
            st.markdown(f"""
            <div class="info-card">
                <h3 style="margin-top: 0; color: #5C7CFA;">Kategori Latihan: {program_pilihan['kategori']}</h3>
                <p style="color: #e0e0e0; text-align: justify; margin-bottom: 0;">{program_pilihan['deskripsi']}</p>
            </div>
            """, unsafe_allow_html=True)

            # 2. TAMPILKAN PRINSIP LATIHAN
            st.markdown("#### 📋 Prinsip Latihan")
            prinsip_html = "<ul style='color: #e0e0e0;'>"
            for prinsip in program_pilihan['prinsip_latihan']:
                prinsip_html += f"<li style='margin-bottom: 8px;'>{prinsip}</li>"
            prinsip_html += "</ul>"
            st.markdown(prinsip_html, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)

            # 3. DROPDOWN (EXPANDER) - BERURUTAN KE BAWAH
            
            # --- Dropdown A: Daftar Latihan ---
            with st.expander("🏋️‍♂️ Daftar Latihan Lengkap", expanded=False):
                for kelompok in program_pilihan["daftar_latihan"]:
                    judul_kelompok = kelompok.get("kelompok_otot") or kelompok.get("jenis")
                    st.markdown(f"<h5 style='color: #5C7CFA;'>{judul_kelompok}</h5>", unsafe_allow_html=True)
                    
                    if "catatan" in kelompok:
                        st.caption(f"📝 *{kelompok['catatan']}*")
                        
                    for gerakan in kelompok["gerakan"]:
                        metrik = gerakan.get("set_rep") or gerakan.get("interval") or gerakan.get("durasi")
                        st.markdown(f"**{gerakan['nama']}** `(Target: {metrik})`")
                        st.markdown(f"<p style='font-size: 0.9em; color: #d1d5db; margin-top:-10px; margin-bottom: 15px;'>{gerakan['cara_melakukan']}</p>", unsafe_allow_html=True)
                    st.divider()

            # --- Dropdown B: Jadwal Mingguan ---
            with st.expander("📅 Rekomendasi Jadwal Mingguan", expanded=False):
                # Membangun tabel secara manual dengan Markdown agar gaya CSS teraplikasi rapi
                tabel_md = "| Hari | Fokus | Detail Latihan |\n|---|---|---|\n"
                for jadwal in program_pilihan["jadwal_mingguan"]:
                    tabel_md += f"| **{jadwal['hari']}** | {jadwal['fokus']} | {jadwal['latihan']} |\n"
                
                st.markdown(tabel_md)

            # --- Dropdown C: Tips Umum ---
            with st.expander("💡 Tips Umum & Keselamatan", expanded=False):
                for key, value in tips_umum.items():
                    judul_tips = key.replace('_', ' ').title()
                    st.markdown(f"**{judul_tips}**")
                    st.markdown(f"<p style='font-size: 0.9em; color: #d1d5db; margin-top:-10px; margin-bottom: 15px;'>{value}</p>", unsafe_allow_html=True)

        else:
            st.error("Gagal memuat data latihan dari JSON.")

st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 0.8em; color: #e0e0e0; font-weight: 500;'>Selalu konsultasikan program latihan dengan profesional bersertifikat</p>", unsafe_allow_html=True)
