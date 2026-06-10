import streamlit as st


def show_result():
    st.markdown("""
        <style>
        .stAppViewMain {
            background-color: #EEF2FF !important;
        }
        .result-screen {
            max-width: 900px;
            margin: 0 auto;
            padding: 34px 16px 40px 16px;
        }
        .result-card {
            background-color: #FFFFFF !important;
            border-radius: 28px !important;
            padding: 40px 40px 32px 40px !important;
            box-shadow: 0 20px 60px rgba(15, 23, 42, 0.08) !important;
            border: 1px solid rgba(99, 102, 241, 0.12) !important;
            margin-bottom: 28px;
        }
        .result-badge {
            width: 72px;
            height: 72px;
            border-radius: 50%;
            background: linear-gradient(180deg, rgba(124, 58, 237, 0.16), rgba(124, 58, 237, 0.04));
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 20px auto;
            font-size: 28px;
        }
        .result-title {
            text-align: center;
            color: #0F172A;
            font-size: 30px;
            font-weight: 800;
            margin-bottom: 12px;
        }
        .result-subtitle {
            text-align: center;
            color: #64748B;
            font-size: 15px;
            margin-bottom: 24px;
            line-height: 1.7;
        }
        .highlight-card {
            background-color: #F8FAFC;
            border-radius: 22px;
            padding: 22px;
            border: 1px solid rgba(99, 102, 241, 0.18);
            box-shadow: 0 14px 40px rgba(15, 23, 42, 0.06);
            margin-bottom: 24px;
        }
        .highlight-card h3 {
            margin: 0 0 8px 0;
            color: #4F46E5;
            font-size: 22px;
            font-weight: 800;
        }
        .highlight-card p {
            margin: 0;
            color: #475569;
            line-height: 1.7;
            font-size: 14px;
        }
        .mini-card {
            background-color: #FFFFFF;
            border-radius: 22px;
            padding: 24px;
            border: 1px solid #F1F5F9;
            box-shadow: 0 14px 36px rgba(15, 23, 42, 0.06);
            min-height: 240px;
        }
        .mini-card h4 {
            margin-bottom: 16px;
            color: #0F172A;
            font-size: 18px;
            font-weight: 800;
        }
        .mini-card li {
            margin-bottom: 10px;
            color: #475569;
            font-size: 14px;
            line-height: 1.8;
        }
        .restart-button {
            max-width: 240px;
            margin: 24px auto 0 auto;
        }
        .stButton > button {
            background-color: #7C3AED !important;
            color: #FFFFFF !important;
            border-radius: 999px !important;
            border: none !important;
            font-weight: 700 !important;
            font-size: 14px !important;
            padding: 0.8rem 1.6rem !important;
            min-height: 48px !important;
            width: 100% !important;
        }
        .stButton > button:hover {
            background-color: #6D28D9 !important;
        }
        @media (max-width: 768px) {
            .result-card { padding: 28px 24px 26px 24px !important; }
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="result-screen">
            <div class="result-card">
                <div class="result-badge">✨</div>
                <div class="result-title">Hasil Rekomendasimu</div>
                <div class="result-subtitle">Berdasarkan profil unikmu, inilah rekomendasi jurusan dan jalur karier yang cocok untukmu.</div>
            </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="highlight-card">
            <h3>Sarjana Ilmu Komputer</h3>
            <p>Fokus pada analisis data, pengembangan perangkat lunak, algoritma, dan pemrograman sistem untuk menciptakan solusi inovatif.</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap='large')
    with col1:
        st.markdown("""
            <div class="mini-card">
                <h4>Potensi Jalur Karier</h4>
                <ul>
                    <li>Software Engineer</li>
                    <li>Data Scientist</li>
                    <li>Artificial Intelligence Engineer</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="mini-card">
                <h4>Keahlian yang Dikuasai</h4>
                <ul>
                    <li>Pemrograman & Algoritma</li>
                    <li>Manajemen Basis Data</li>
                    <li>Machine Learning</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("""
            <div class="restart-button">
    """, unsafe_allow_html=True)

    if st.button('🔄 Mulai Ulang', use_container_width=True):
        st.session_state.page = 'home'
        st.session_state.current_step = 1
        st.session_state.answers = {}
        st.rerun()

    st.markdown("""
            </div>
        </div>
    """, unsafe_allow_html=True)
