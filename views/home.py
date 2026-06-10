import streamlit as st
import base64
import os

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    return ""

def show_home():
    # Mengambil resource lokal gambar
    img_topi = get_image_base64("assets/graduation.png")
    img_analisis = get_image_base64("assets/personalization.png")
    img_rekomendasi = get_image_base64("assets/student.png")
    img_karier = get_image_base64("assets/mentorship.png")
    
    img_btn_left = get_image_base64("assets/shining.png") 
    img_btn_right = get_image_base64("assets/right_arrow.png")
    
    # 1. CSS Global Murni (Tanpa f-string agar VS Code tidak membaca sebagai variabel error)
    st.html("""
        <style>
        .stAppViewMain {
            background-color: #EEF2FF !important;
        }
        
        .stButton>button {
            background-color: #7C3AED !important;
            color: white !important;
            border-radius: 999px !important;
            border: none !important;
            padding: 0.6rem 2.5rem !important;
            font-weight: 700 !important;
            font-size: 16px !important;
            box-shadow: 0 6px 20px rgba(124, 58, 237, 0.25) !important;
            transition: all 0.3s ease;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            gap: 10px !important;
        }
        
        .stButton>button:hover {
            background-color: #6D28D9 !important;
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(124, 58, 237, 0.35) !important;
        }
        
        .home-container {
            text-align: center;
            font-family: 'Source Sans Pro', sans-serif;
            padding-top: 20px;
        }
        
        .icon-circle {
            background-color: #7C3AED;
            width: 100px;
            height: 100px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 24px auto;
            box-shadow: 0 8px 24px rgba(124, 58, 237, 0.2);
        }
        
        .feature-card {
            background-color: white;
            padding: 24px;
            border-radius: 16px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.02);
            height: 100%;
            min-height: 220px;
            border: 1px solid #F1F5F9;
            text-align: left;
        }
        .feature-icon {
            margin-bottom: 16px;
        }
        .feature-title {
            font-size: 16px;
            font-weight: 700;
            color: #0F172A;
            margin-bottom: 8px;
        }
        .feature-desc {
            font-size: 13px;
            color: #64748B;
            line-height: 1.6;
        }
        
        .how-it-works-section {
            background-color: white;
            border-radius: 20px;
            padding: 40px 30px;
            margin-top: 40px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.02);
            border: 1px solid #F1F5F9;
        }
        .section-title {
            font-size: 18px;
            font-weight: 700;
            color: #0F172A;
            margin-bottom: 36px;
            text-align: center;
        }
        
        .step-item {
            text-align: center;
        }
        .step-number {
            background-color: #F5F3FF;
            color: #7C3AED;
            width: 36px;
            height: 36px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 14px;
            margin: 0 auto 12px auto;
        }
        .step-label {
            font-size: 14px;
            font-weight: 700;
            color: #0F172A;
            margin-bottom: 6px;
        }
        .step-desc {
            font-size: 12px;
            color: #64748B;
            line-height: 1.5;
        }
        
        .main-title {
            color: #1E1B4B;
            font-size: 36px;
            font-weight: 800;
            margin-bottom: 16px;
        }
        .sub-title {
            color: #64748B;
            font-size: 15px;
            max-width: 600px;
            margin: 0 auto 36px auto;
            line-height: 1.6;
        }
        .footer-note {
            text-align: center;
            color: #94A3B8;
            font-size: 13px;
            margin-top: 32px;
        }
        </style>
    """)

    # 2. CSS Khusus Ikon Tombol (Menggunakan f-string secara terpisah & minimalis)
    st.html(f"""
        <style>
        .stButton>button::before {{
            content: "" !important;
            display: inline-block !important;
            width: 18px !important;
            height: 18px !important;
            background-image: url("data:image/png;base64,{img_btn_left}") !important;
            background-size: contain !important;
            background-repeat: no-repeat !important;
            background-position: center !important;
        }}
        
        .stButton>button::after {{
            content: "" !important;
            display: inline-block !important;
            width: 18px !important;
            height: 18px !important;
            background-image: url("data:image/png;base64,{img_btn_right}") !important;
            background-size: contain !important;
            background-repeat: no-repeat !important;
            background-position: center !important;
        }}
        </style>
    """)

    # Render Judul Utama dan Sub-judul
    st.markdown(f"""
        <div class='home-container'>
            <div class='icon-circle'>
                <img src="data:image/png;base64,{img_topi}" style="width: 50px; height: 50px; object-fit: contain;">
            </div>
            <div class='main-title'>Career & Education Pathway</div>
            <div class='sub-title'>Discover your ideal bachelor's degree and career path through a personalized assessment of your hobis, interest, and goals</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Render Tombol Navigasi
    _, col_btn, _ = st.columns([1.2, 1.6, 1.2])
    with col_btn:
        if st.button("Start Your Journey", use_container_width=True):
            st.session_state.page = 'question'
            st.rerun()

    st.write("<br>", unsafe_allow_html=True)

    # Render Tiga Kartu Fitur Utama
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
            <div class='feature-card'>
                <div class='feature-icon'><img src="data:image/png;base64,{img_analisis}" style="width: 36px; height: 36px;"></div>
                <div class='feature-title'>Analisis Personal</div>
                <div class='feature-desc'>Penilaian cerdas yang menganalisis hobi, bakat, dan preferensimu untuk memberikan saran yang tepat.</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
            <div class='feature-card'>
                <div class='feature-icon'><img src="data:image/png;base64,{img_rekomendasi}" style="width: 36px; height: 36px;"></div>
                <div class='feature-title'>Rekomendasi Pendidikan</div>
                <div class='feature-desc'>Temukan jurusan dan program studi yang paling sesuai dengan kemampuan dan minat akademismu.</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
            <div class='feature-card'>
                <div class='feature-icon'><img src="data:image/png;base64,{img_karier}" style="width: 36px; height: 36px;"></div>
                <div class='feature-title'>Jalur Karier</div>
                <div class='feature-desc'>Jelajahi berbagai pilihan karier yang selaras dengan jurusan pilihanmu dan cita-cita jangka panjang.</div>
            </div>
        """, unsafe_allow_html=True)

    # Render Bagian Cara Kerja (4 Langkah)
    st.markdown("<div class='how-it-works-section'><div class='section-title'>Cara Kerja</div>", unsafe_allow_html=True)
    
    step_col1, step_col2, step_col3, step_col4 = st.columns(4)
    with step_col1:
        st.markdown("""
            <div class='step-item'>
                <div class='step-number'>1</div>
                <div class='step-label'>Jawab Pertanyaan</div>
                <div class='step-desc'>Menjawab pertanyaan seputar hobi, bakat, dan minatmu</div>
            </div>
        """, unsafe_allow_html=True)
    with step_col2:
        st.markdown("""
            <div class='step-item'>
                <div class='step-number'>2</div>
                <div class='step-label'>Isi Preferensi</div>
                <div class='step-desc'>Sampaikan gaya belajar dan cara bekerja favoritmu</div>
            </div>
        """, unsafe_allow_html=True)
    with step_col3:
        st.markdown("""
            <div class='step-item'>
                <div class='step-number'>3</div>
                <div class='step-label'>Dapatkan Analisis</div>
                <div class='step-desc'>Algoritma kami memproses profilmu</div>
            </div>
        """, unsafe_allow_html=True)
    with step_col4:
        st.markdown("""
            <div class='step-item'>
                <div class='step-number'>4</div>
                <div class='step-label'>Lihat Hasil</div>
                <div class='step-desc'>Terima rekomendasi yang dipersonalisasi untukmu</div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div class='footer-note'>Hanya membutuhkan waktu 5 menit, Gratis, Tidak perlu registrasi</div>", unsafe_allow_html=True)