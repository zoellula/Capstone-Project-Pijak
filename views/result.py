import streamlit as st
from views.kamus import (jurusan_dict, ekskul_dict, personality_dict, hobi_dict,
                         get_jurusan_populer_text)


def reset_state():
    """Reset semua jawaban dan kembali ke halaman awal."""
    for key in ['minat', 'hard_skill', 'soft_skill', 'mapel',
                'jurusan_sekolah', 'personality', 'hobi', 'ekskul']:
        if key in st.session_state:
            st.session_state[key] = '' if isinstance(st.session_state[key], str) else []

    st.session_state.page = 'home'
    #st.rerun()


def _normalize_list(value):
    if isinstance(value, str):
        return [value] if value else []
    if isinstance(value, list):
        return [item for item in value if item]
    return []


def show_result():
    model = st.session_state.get('model')
    tfidf = st.session_state.get('tfidf')
    le = st.session_state.get('le')

    minat = st.session_state.get('minat', '')
    hard_skill_list = st.session_state.get('hard_skill', [])
    soft_skill_list = st.session_state.get('soft_skill', [])
    mapel_list = st.session_state.get('mapel', [])
    if isinstance(mapel_list, str):
        mapel_list = [mapel_list] if mapel_list else []
    mapel = " ".join(mapel_list)

    
    if model is None or tfidf is None or le is None:
        st.error("Model prediksi belum dimuat. Silakan muat ulang halaman atau kembali ke beranda.")
        if st.button("Kembali ke Beranda"):
            st.session_state.page = 'home'
            st.rerun()
        return

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
        
    jurusan_selected = st.session_state.get('jurusan_sekolah', [])
    if isinstance(jurusan_selected, str):
        jurusan_selected = [jurusan_selected]
    for opt in jurusan_selected:
        for bidang in jurusan_dict.get(opt, []):
            skor[bidang] += 15

    hobi_selected = st.session_state.get('hobi', [])
    if isinstance(hobi_selected, str):
        hobi_selected = [hobi_selected]
    for opt in hobi_selected:
        for bidang in hobi_dict.get(opt, []):
            skor[bidang] += 10

    ekskul_selected = st.session_state.get('ekskul', [])
    if isinstance(ekskul_selected, str):
        ekskul_selected = [ekskul_selected]
    for opt in ekskul_selected:
        for bidang in ekskul_dict.get(opt, []):
            skor[bidang] += 5

    personality_selected = st.session_state.get('personality', [])
    if isinstance(personality_selected, str):
        personality_selected = [personality_selected]
    for opt in personality_selected:
        for bidang in personality_dict.get(opt, []):
            skor[bidang] += 10


    # --- C. HASIL AKHIR (Top 3) ---
    ranking = sorted(skor.items(), key=lambda x: x[1], reverse=True)
    total_skor = sum(skor.values()) if sum(skor.values()) > 0 else 1 
    top_3 = ranking[:3]

    # --- D. TAMPILAN UI ---
    st.header("Hasil Rekomendasi")
    st.markdown("---")
    st.write("Berdasarkan **Analisis Potensi Utama (AI) & Profil Keseharianmu**, ini adalah 3 bidang yang paling cocok untukmu. Klik setiap bidang untuk melihat jurusan populer yang sesuai dengan minat dan keahlianmu!")

    #st.success(f"🥇 **{top_3[0][0]}** — {round((top_3[0][1] / total_skor) * 100, 2)}%")
    #st.info(f"🥈 **{top_3[1][0]}** — {round((top_3[1][1] / total_skor) * 100, 2)}%")
    #st.warning(f"🥉 **{top_3[2][0]}** — {round((top_3[2][1] / total_skor) * 100, 2)}%")

    #st.markdown("---")
    #st.subheader("Jurusan Populer untuk Setiap Rekomendasi")

    for idx, (bidang, skor_bidang) in enumerate(top_3, start=1):
        pct = round((skor_bidang / total_skor) * 100, 2)
        emoji = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉"
        accent = "#16A34A" if idx == 1 else "#3B82F6" if idx == 2 else "#F59E0B"
        st.markdown(
            f"""
            <style>
            div[data-testid="stExpander"]:nth-of-type({idx}) > button {{
                background: {accent} !important;
                color: white !important;
                border-radius: 14px !important;
                font-weight: 700 !important;
            }}
            div[data-testid="stExpander"]:nth-of-type({idx}) > button:hover {{
                filter: brightness(0.95) !important;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )
        with st.expander(f"{emoji} {bidang} — {pct}% cocok", expanded=(idx == 0)):
            st.markdown(get_jurusan_populer_text(bidang), unsafe_allow_html=True)

    st.write("### Apa langkah selanjutnya?")
    st.write(
        f"Bidang utama yang paling direkomendasikan adalah **{top_3[0][0]}**, "
        f"namun kamu juga memiliki potensi kuat di **{top_3[1][0]}** dan **{top_3[2][0]}**. "
        "Cobalah mencari tahu lebih dalam tentang program studi atau profesi di ketiga bidang ini. "
        "Jangan ragu untuk mendiskusikannya dengan guru BK atau orang tuamu untuk memantapkan pilihan!"
    )

    with st.expander("📌 Ringkasan Jawabanmu", expanded=False):
        st.write(f"**Minat yang dipilih:** {', '.join(_normalize_list(st.session_state.get('minat', ''))).title() or '-'}")
        st.write(f"**Keahlian teknis yang dipilih:** {', '.join(_normalize_list(st.session_state.get('hard_skill', []))).title() or '-'}")
        st.write(f"**Keterampilan personal yang dipilih:** {', '.join(_normalize_list(st.session_state.get('soft_skill', []))).title() or '-'}")
        st.write(f"**Pelajaran favorit yang dipilih:** {', '.join(_normalize_list(st.session_state.get('mapel', []))).title() or '-'}")
        st.write(f"**Jurusan sekolah:** {', '.join(_normalize_list(st.session_state.get('jurusan_sekolah', []))).title() or '-'}")
        st.write(f"**Kepribadian:** {', '.join(_normalize_list(st.session_state.get('personality', []))).title() or '-'}")
        st.write(f"**Hobi:** {', '.join(_normalize_list(st.session_state.get('hobi', []))).title() or '-'}")
        st.write(f"**Ekstrakurikuler:** {', '.join(_normalize_list(st.session_state.get('ekskul', []))).title() or '-'}")

    st.markdown("---")
    st.button("🔄 Ulangi Tes", on_click=reset_state)