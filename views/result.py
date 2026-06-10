import streamlit as st
from views.kamus import (jurusan_dict, ekskul_dict, personality_dict, hobi_dict,
                         get_jurusan_populer_text)

def show_result():
    model = st.session_state.get('model')
    tfidf = st.session_state.get('tfidf')
    le = st.session_state.get('le')

    minat = st.session_state.get('minat', '')
    hard_skill_list = st.session_state.get('hard_skill', [])
    soft_skill_list = st.session_state.get('soft_skill', [])
    mapel = st.session_state.get('mapel', '')
    
    if minat == '' or len(hard_skill_list) == 0:
        st.warning("Sepertinya kamu belum menyelesaikan tes! Yuk, mulai dari awal.")
        if st.button("Kembali ke Beranda"):
            st.session_state.page = 'home'
            st.rerun()
        return

    # --- A. PREDIKSI ML ---
    hard_skill_str = " ".join(hard_skill_list)
    soft_skill_str = " ".join(soft_skill_list)
    teks_gabungan = f"{minat} {hard_skill_str} {soft_skill_str} {mapel}"
    
    input_tfidf = tfidf.transform([teks_gabungan])
    prediksi_ml = model.predict(input_tfidf)
    prediksi_rf = str(le.inverse_transform(prediksi_ml)[0])

    # --- B. PERHITUNGAN SKOR PENDUKUNG ---
    skor = {
        "Komputer dan Teknologi": 0, "Teknik": 0, "Kesehatan": 0,
        "Ekonomi dan Bisnis": 0, "Pendidikan": 0, "Seni": 0,
        "Sosial dan Humaniora": 0, "Pertanian": 0, "Sains dan MIPA": 0
    }
    
    if prediksi_rf in skor:
        skor[prediksi_rf] += 20
        
    for bidang in jurusan_dict.get(st.session_state.get('jurusan_sekolah'), []):
        skor[bidang] += 15
    for bidang in hobi_dict.get(st.session_state.get('hobi'), []):
        skor[bidang] += 10
    for bidang in ekskul_dict.get(st.session_state.get('ekskul'), []):
        skor[bidang] += 5
    for bidang in personality_dict.get(st.session_state.get('personality'), []):
        skor[bidang] += 10

    # --- C. HASIL AKHIR (Top 3) ---
    ranking = sorted(skor.items(), key=lambda x: x[1], reverse=True)
    total_skor = sum(skor.values()) if sum(skor.values()) > 0 else 1 
    top_3 = ranking[:3]

    # --- D. TAMPILAN UI ---
    st.markdown("""
        <style>
        .result-screen { max-width: 900px; margin: 0 auto; padding: 20px; }
        .result-card { background-color: #FFFFFF; border-radius: 28px; padding: 40px; box-shadow: 0 20px 60px rgba(15, 23, 42, 0.08); text-align: center; margin-bottom: 24px; }
        .badge-1 { font-size: 40px; margin-bottom: 10px; }
        .top-1 { color: #4F46E5; font-size: 28px; font-weight: 800; margin-bottom: 5px; }
        .mini-card { background-color: #F8FAFC; border-radius: 22px; padding: 20px; text-align: center; border: 1px solid #E2E8F0; }
        </style>
    """, unsafe_allow_html=True)

    pct_1 = round((top_3[0][1]/total_skor)*100, 2)
    pct_2 = round((top_3[1][1]/total_skor)*100, 2)
    pct_3 = round((top_3[2][1]/total_skor)*100, 2)

    st.markdown(f"""
        <div class="result-screen">
            <div class="result-card">
                <div class="badge-1">🏆</div>
                <div style="color: #64748B; font-size: 16px;">Rekomendasi Utama Kamu</div>
                <div class="top-1">{top_3[0][0]}</div>
                <div style="font-size: 18px; font-weight: bold; color: #10B981;">Kecocokan: {pct_1}%</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
            <div class="mini-card">
                <div style="font-size: 24px;">🥈</div>
                <h4 style="margin: 10px 0; color: #334155;">{top_3[1][0]}</h4>
                <div style="color: #64748B;">Kecocokan: {pct_2}%</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="mini-card">
                <div style="font-size: 24px;">🥉</div>
                <h4 style="margin: 10px 0; color: #334155;">{top_3[2][0]}</h4>
                <div style="color: #64748B;">Kecocokan: {pct_3}%</div>
            </div>
        """, unsafe_allow_html=True)

    st.write("<br>", unsafe_allow_html=True)
    st.subheader("💡 Jurusan Populer di Bidang Tersebut")
    st.info(f"**{top_3[0][0]}**: {get_jurusan_populer_text(top_3[0][0])}")

    st.write("<br>", unsafe_allow_html=True)
    if st.button('🔄 Mulai Ulang Tes', use_container_width=True):
        # Reset jawaban kuesioner ke default dari kamus
        for key in ['minat', 'hard_skill', 'soft_skill', 'mapel', 'jurusan_sekolah', 'personality', 'hobi', 'ekskul']:
            if key in st.session_state:
                st.session_state[key] = '' if isinstance(st.session_state[key], str) else []
        st.session_state.page = 'home'
        st.rerun()