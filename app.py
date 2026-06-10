import streamlit as st
import pandas as pd
import numpy as np
import pickle # Tambahan dari backend untuk membaca file model

# Import fungsi halaman dari folder views
from views.home import show_home
from views.question import show_question
from views.result import show_result

# --- KONFIGURASI HALAMAN & THEME ---
st.set_page_config(page_title="Career & Education Pathway", page_icon="🎓", layout="centered")

# --- MEMUAT MODEL ML (DARI BACKEND) ---
@st.cache_resource
def load_models():
    try:
        # Catatan: Jika file .pkl kamu ada di dalam folder 'Model', 
        # ubah menjadi 'Model/model_pijak.pkl' dst.
        with open('model_pijak.pkl', 'rb') as file:
            model = pickle.load(file)
        with open('tfidf_pijak.pkl', 'rb') as file:
            tfidf = pickle.load(file)
        with open('label_encoder.pkl', 'rb') as file:
            le = pickle.load(file)
        return model, tfidf, le
    except Exception as e:
        st.error(f"Gagal memuat model: {e}")
        return None, None, None

# Panggil fungsinya
model, tfidf, le = load_models()

# Simpan model ke dalam brankas session_state agar bisa diakses oleh folder views
if 'model' not in st.session_state:
    st.session_state.model = model
if 'tfidf' not in st.session_state:
    st.session_state.tfidf = tfidf
if 'le' not in st.session_state:
    st.session_state.le = le

# Custom CSS global 
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

# --- INISIALISASI SESSION STATE (NAVIGASI & VARIABEL JAWABAN) ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Siapkan tempat kosong untuk menampung jawaban pengguna dari kuesioner
state_keys = {
    'minat': '', 'hard_skill': [], 'soft_skill': [], 'mapel': '',
    'jurusan_sekolah': '', 'personality': '', 'hobi': '', 'ekskul': ''
}
for key, default_value in state_keys.items():
    if key not in st.session_state:
        st.session_state[key] = default_value

# --- KONTROL NAVIGASI HALAMAN ---
if st.session_state.page == 'home':
    show_home()
elif st.session_state.page == 'question':
    # Halaman kuesioner dinamis
    show_question()
elif st.session_state.page == 'result':
    show_result()