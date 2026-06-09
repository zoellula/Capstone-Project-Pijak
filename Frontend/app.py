import streamlit as st

# Import fungsi halaman dari folder views (Cukup panggil show_question yang dinamis)
from views.home import show_home
from views.question import show_question
from views.result import show_result

# --- KONFIGURASI HALAMAN & THEME ---
st.set_page_config(page_title="Career & Education Pathway", page_icon="🎓", layout="centered")

# Custom CSS global (Tetap dipertahankan untuk kebutuhan umum)
st.markdown("""
    <style>
    .stButton>button {
        background-color: #6366F1;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #4F46E5;
        color: white;
    }
    .card-box {
        background-color: #F8FAFC;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #E2E8F0;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- INISIALISASI SESSION STATE (NAVIGASI) ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- KONTROL NAVIGASI HALAMAN ---
if st.session_state.page == 'home':
    show_home()
elif st.session_state.page == 'question':
    # Halaman kuesioner dinamis yang membaca dataset kamu
    show_question()
elif st.session_state.page == 'result':
    show_result()