import streamlit as st
import pandas as pd
import base64
import os

def get_base64_image(path):
    with open(path, "rb") as img:
        return base64.b64encode(img.read()).decode()

@st.cache_data
def load_questions():
    path = "data/questions.csv"
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame({
        'question_id': [1, 2],
        'question_text': ["Apa Hobi mu?", "Bagaimana Caramu Belajar?"],
        'sub_text': ["pilih maksimal 3 hobi", "pilih cara belajar yang paling kamu sukai"],
        'type': ["multiple", "single"],
        'options': [
            "Membaca & Menulis,Olahraga,Koding,Seni & Desain,Bisnis,Musik,Fotografi,Traveling,Memasak,Gaming",
            "Visual dan Media Interaktif,Mendengarkan Penjelasan,Praktik Langsung,Diskusi Kelompok"
        ]
    })

def show_question():
    df_questions = load_questions()
    total_steps = len(df_questions)
    shine_img = get_base64_image("assets/shining.png")


    if 'current_step' not in st.session_state:
        st.session_state.current_step = 1
    if 'answers' not in st.session_state:
        st.session_state.answers = {}

    current_idx = max(0, min(st.session_state.current_step - 1, total_steps - 1))
    q_row = df_questions.iloc[current_idx]
    q_id = int(q_row['question_id'])
    q_text = q_row['question_text']
    q_type = q_row.get('type', 'multiple')
    q_sub = q_row.get('sub_text', 'pilih jawaban yang paling sesuai')
    options_list = [opt.strip() for opt in str(q_row['options']).split(',')]
    progress_percentage = int((st.session_state.current_step / total_steps) * 100)
    
    st.markdown("""
        <style>
        /* Background Utama Aplikasi */
        .stApp {
            background-color: #EEF2FF !important;
        }
        
        /* Kartu Putih Utama Kuesioner */
        .question-card {
            background-color: #FFFFFF !important;
            border-radius: 24px !important;
            padding: 40px 40px 40px 40px !important;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.04) !important;
            border: 1px solid rgba(99, 102, 241, 0.08) !important;
            margin-bottom: 24px !important;
        }
        
        /* Teks Progress */
        .step-text {
            color: #94A3B8;
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 8px;
        }
        
        /* Judul & Subjudul Pertanyaan */
        .question-title {
            color: #0F172A !important;
            font-size: 30px !important;
            font-weight: 800 !important;
            margin-top: 15px !important;
            margin-bottom: 6px !important;
            font-family: 'Source Sans Pro', sans-serif;
        }
        .question-subtitle {
            color: #94A3B8 !important;
            font-size: 13px !important;
            margin-bottom: 32px !important;
        }
        
        /* Progress Bar Custom */
        .stProgress > div > div > div > div {
            background-color: #6366F1 !important;
            border-radius: 999px !important;
        }
        .stProgress {
            height: 8px !important;
            margin-bottom: 28px !important;
        }
        
        /* --- KUSTOMISASI STYLES CHECKBOX (MULTIPLE CHOICE) --- */
        div[data-testid="stCheckbox"] {
            background-color: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 14px !important;
            padding: 0px 18px !important;
            margin-bottom: 12px !important;
            transition: all 0.2s ease-in-out !important;
            min-height: 58px !important;
            width:320px !important;
            display: flex !important;
            align-items: center !important;
        }
        /* Efek saat dipilih */
        div[data-testid="stCheckbox"]:hover {
            border-color: #CBD5E1 !important;
        }
       div[data-testid="stCheckbox"]:has(input:checked){
            border-color:#7C3AED !important;
            box-shadow:0 4px 12px rgba(124,58,237,.08) !important;
        }
        div[data-testid="stCheckbox"] label {
            width: 100% !important;
            display: flex !important;
            align-items: center !important;
            gap: 14px !important;
        }
        div[data-testid="stCheckbox"] label p {
            color: #334155 !important;
            font-weight: 600 !important;
            font-size: 15px !important;
            margin: 0 !important;
        }     
        
        /* --- KUSTOMISASI STYLES RADIO (SINGLE CHOICE) --- */
        div[data-testid="stRadio"] > div {
            gap: 12px !important;
            width: 700px !important;
        }
        div[data-testid="stRadio"] label {
            background-color: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 14px !important;
            padding: 0px 18px !important;
            margin: 0 0 12px 0 !important;
            transition: all 0.2s ease-in-out !important;
            min-height: 58px !important;
            display: flex !important;
            align-items: center !important;
            gap: 14px !important;
            width: 700px !important;
        }
        div[data-testid="stRadio"] > label{
            display:none !important;
        }
        div[data-testid="stRadio"] label:hover {
            border-color: #CBD5E1 !important;
        }
        div[data-testid="stRadio"] label:has(input[type="radio"]:checked) {
            border-color: #7C3AED !important;
            background-color: #FFFFFF !important;
            box-shadow: 0 4px 12px rgba(124, 58, 237, 0.05) !important;
        }
        div[data-testid="stRadio"] label p {
            color: #334155 !important;
            font-weight: 600 !important;
            font-size: 15px !important;
            margin: 0 !important;
        }
        /* radio yang terpilih */
        div[data-testid="stRadio"] svg {
            fill: #7C3AED !important;
        }

        /* lingkaran radio */
        div[data-testid="stRadio"] [role="radio"][aria-checked="true"] {
            background-color: #7C3AED !important;
            border-color: #7C3AED !important;
        }
        
        /* --- TOMBOL NAVIGASI NAV --- */
        div[data-testid="stButton"] > button {
            border-radius: 12px !important;
            font-weight: 700 !important;
            font-size: 14px !important;
            min-height: 46px !important;
            width: 100% !important;
            transition: all 0.2s ease;
        }
        /* Tombol Sebelumnya (Putih) */
        div[data-testid="stHorizontalBlock"] > div:first-child .stButton > button {
            background-color: #FFFFFF !important;
            color: #64748B !important;
            border: 1px solid #E2E8F0 !important;
        }
        div[data-testid="stHorizontalBlock"] > div:first-child .stButton > button:hover {
            border-color: #CBD5E1 !important;
            color: #475569 !important;
        }
        /* Tombol Selanjutnya / Lihat Hasil (Ungu) */
        div[data-testid="stHorizontalBlock"] > div:last-child .stButton > button {
            background-color: #7C3AED !important;
            color: #FFFFFF !important;
            border: none !important;
        }
        div[data-testid="stHorizontalBlock"] > div:last-child .stButton > button:hover {
            background-color: #6D28D9 !important;
        }

        .result-btn {
            width:100%;
            background:#7C3AED;
            color:white;
            border:none;
            border-radius:12px;
            height:46px;
            display:flex;
            align-items:center;
            justify-content:center;
            gap:10px;
            font-weight:700;
            cursor:pointer;
        }
        .result-btn img {
            width:20px;
            height:20px;
        }
        
        </style>
    """, unsafe_allow_html=True)
    st.markdown(f"""
        <style>
        div[data-testid="stHorizontalBlock"] > div:last-child .stButton > button::before{{
            content:"";
            display:inline-block;
            width:18px;
            height:18px;
            margin-right:8px;

            background-image:url("data:image/png;base64,{shine_img}");
            background-size:contain;
            background-repeat:no-repeat;
            background-position:center;
        }}
        </style>
    """, unsafe_allow_html=True)

    # Struktur Baris Atas: Progress dan Keterangan Step
    step_column, percent_column = st.columns([4, 1])
    with step_column:
        st.markdown(f"<div class='step-text'>Step {st.session_state.current_step} dari {total_steps} ...</div>", unsafe_allow_html=True)
    with percent_column:
        st.markdown(f"<div class='step-text' style='text-align: right;'>{progress_percentage}%</div>", unsafe_allow_html=True)

    # Render Progress Bar Streamlit
    st.progress(st.session_state.current_step / total_steps)

    # Membuka pembungkus container kartu putih
    st.markdown(f"""
        <div class="question-card">
            <div class="question-title">{q_text}</div>
            <div class="question-subtitle">{q_sub}</div>
    """, unsafe_allow_html=True)

    # Alur Pilihan Ganda Banyak Jawaban (Multiple)
    if q_type == 'multiple':
        if q_id not in st.session_state.answers or not isinstance(st.session_state.answers[q_id], list):
            st.session_state.answers[q_id] = []

        selected_options = []
        # Grid 2 Kolom Pilihan Sejajar sesuai Desain Figma
        cols = st.columns(2, gap='medium')
        for idx, option in enumerate(options_list):
            with cols[idx % 2]:
                is_checked = option in st.session_state.answers[q_id]
                if st.checkbox(option, value=is_checked, key=f'q_{q_id}_opt_{idx}'):
                    selected_options.append(option)
        st.session_state.answers[q_id] = selected_options
    
    # Alur Pilihan Ganda Tunggal (Single/Radio)
    else:
        if q_id not in st.session_state.answers or isinstance(st.session_state.answers[q_id], list):
            st.session_state.answers[q_id] = options_list[0]

        try:
            default_idx = options_list.index(st.session_state.answers[q_id])
        except ValueError:
            default_idx = 0

        chosen_radio = st.radio(
            " ",
            options=options_list,
            index=default_idx,
            key=f'q_{q_id}_radio',
            label_visibility="collapsed"
        )
        st.session_state.answers[q_id] = chosen_radio

    # Menutup tag kontainer kartu putih sebelum masuk ke tombol navigasi
    st.markdown('</div>', unsafe_allow_html=True)

    # Baris Navigasi Tombol di bagian bawah luar card putih
    nav_left, nav_right = st.columns([1, 1], gap='medium')
    with nav_left:
        if st.session_state.current_step > 1:
            if st.button('<  Sebelumnya', use_container_width=True):
                st.session_state.current_step -= 1
                st.rerun()
        else:
            # Placeholder kosong agar posisi tombol kanan tidak bergeser kiri saat di step 1
            st.write("")
            
    with nav_right:
        if st.session_state.current_step < total_steps:
            if st.button('Selanjutnya  >', use_container_width=True):
                st.session_state.current_step += 1
                st.rerun()
        else:
            if st.button('Lihat Hasil', use_container_width=True):
                st.session_state.page = 'result'
                st.rerun()

    # Menutup tag pembungkus utama halaman (.main-wrapper)
    st.markdown('</div>', unsafe_allow_html=True)