import streamlit as st
from views.kamus import (minat_dict, hard_skill_dict, soft_skill_dict, mapel_dict,
                         jurusan_dict, ekskul_dict, personality_dict, hobi_dict, terjemahan_minat,
                         terjemahan_hard, terjemahan_mapel, detail_jurusan,
                         create_minat_accordion, create_checkbox_group, get_selected_checkboxes,
                         create_support_accordion, create_radio_group,
                         create_single_checkbox_group)
import streamlit.components.v1 as components

def scroll_to_top():
    """Force scroll ke posisi paling atas"""
    components.html(
        """
        <script>
            function forceScroll() {
                try {
                    // Method 1: Direct coordinates
                    window.scrollTo(0, 0);
                    
                    // Method 2: Set scroll properties dengan safety check
                    if (document.documentElement) {
                        document.documentElement.scrollTop = 0;
                    }
                    if (document.body) {
                        document.body.scrollTop = 0;
                    }
                } catch(e) {
                    console.error('Scroll error:', e);
                }
            }
            
            // Immediate
            forceScroll();
            
            // Retry dengan delays berbeda
            setTimeout(forceScroll, 50);
            setTimeout(forceScroll, 150);
            setTimeout(forceScroll, 300);
            setTimeout(forceScroll, 600);
            
            // Use requestAnimationFrame
            requestAnimationFrame(forceScroll);
        </script>
        """,
        height=0,
    )

def show_question():
    # Scroll ke atas saat halaman pertama load atau step berubah
    scroll_to_top()

    st.markdown(f"""
    <style>
    html, body {{
        scroll-behavior: auto !important;
        scroll-padding-top: 0 !important;
    }}

    /* === BUTTON KEMBALI & SELANJUTNYA === */
    /* semua button navigasi */
    button[kind="primary"],
    button[kind="secondary"]{{
        height:55px !important;
        border-radius:16px !important;
        font-size:16px !important;
        font-weight:600 !important;
        border:none !important;
        transition:0.3s;
    }}

    /* Selanjutnya */
    button[kind="primary"]{{
        background:#6366F1 !important;
        color:white !important;
    }}

    button[kind="primary"]:hover{{
        background:#4F46E5 !important;
    }}

    /* Kembali */
    button[kind="secondary"]{{
        background:#EEF2FF !important;
        color:#6366F1 !important;
    }}

    button[kind="secondary"]:hover{{
        background:#6366F1 !important;
        color:white !important;
    }}

    /* === PILIHAN MINAT / HARD SKILL / SOFT SKILL ==== */

    div[data-testid="stCheckbox"] input[type="checkbox"]{{
        display:none;
    }}

    div[data-testid="stCheckbox"] label{{
        background:#F3F0FF !important;
        border:1px solid #DDD6FE !important;
        min-width:330px !important;
        min-height:100% !important;
        padding:0.75rem 1.25rem !important;
        display:flex !important;
        align-items:center !important;
        white-space:normal !important;
        word-break:break-word !important;
        box-sizing:border-box !important;
        border-radius:10px !important;
        transition:0.3s;
    }}
                
    div[data-testid="stCheckbox"] label:empty{{
     display:none !important;
    }}

    div[data-testid="stCheckbox"] label p{{
        color:#8B5CF6 !important;
        font-weight:600 !important;
        margin:0 !important;
        line-height:1.2 !important;
    }}

    div[data-testid="stCheckbox"] label:hover{{
        background:#E9D5FF !important;
    }}

    div[data-testid="stCheckbox"]:has(input:checked) label{{
        background:#8B5CF6 !important;
        border-color:#8B5CF6 !important;
    }}

    div[data-testid="stCheckbox"]:has(input:checked) label p{{
        color:white !important;
        font-weight:700 !important;
    }}
    
    div[data-testid="stExpander"] div[data-testid="stButton"] button{{
        background:#8B5CF6 !important;
        color:white !important;
        border:1px solid #8B5CF6 !important;
        border-radius:18px !important;
        min-width:320px !important;
        min-height:50px !important;
        padding:0.75rem 1rem !important;
        font-weight:700 !important;
    }}

    div[data-testid="stExpander"] div[data-testid="stButton"] button:hover{{
        background:#7C3AED !important;
    }}
    
    div[data-testid="stExpander"] summary {{
        font-weight: 800 !important;
        font-size: 18px !important;
        color: #111827 !important;
    }}

    /* === RADIO PILIHAN FITUR PENDUKUNG ==== */
    div[data-testid="stRadio"] input[type="radio"]{{
        display:none;
    }}

    div[data-testid="stRadio"] label{{
        background:#F3F0FF !important;
        border:1px solid #DDD6FE !important;
        min-width:330px !important;
        min-height:100% !important;
        padding:0.75rem 1.25rem !important;
        display:flex !important;
        align-items:center !important;
        white-space:normal !important;
        word-break:break-word !important;
        box-sizing:border-box !important;
        border-radius:10px !important;
        transition:0.3s;
        color:#8B5CF6 !important;
        font-weight:600 !important;
        margin-bottom:0.5rem !important;
    }}

    div[data-testid="stRadio"] label:hover{{
        background:#E9D5FF !important;
    }}

    div[data-testid="stRadio"] label:has(input:checked){{
        background:#8B5CF6 !important;
        border-color:#8B5CF6 !important;
        color:white !important;
        font-weight:700 !important;
    }}

    .question-header{{
        position:sticky;
        top:0;
        z-index:50;
        background:#FFFFFF !important;
        border:1px solid #E5E7EB !important;
        border-radius:24px !important;
        padding:1.5rem 1.5rem 1.25rem !important;
        box-shadow:0 20px 40px rgba(15, 23, 42, 0.08) !important;
        margin-bottom:1.5rem !important;
        animation:fadeIn 0.35s ease-out !important;
    }}

    .step-chip{{
        display:inline-flex;
        align-items:center;
        background:#E0E7FF !important;
        color:#4338CA !important;
        padding:0.5rem 0.85rem !important;
        border-radius:999px !important;
        font-weight:700 !important;
        letter-spacing:0.01em !important;
        margin-bottom:0.75rem !important;
    }}

    .question-title{{
        color:#1E293B !important;
        font-size:3rem !important;
        margin:0 0 0.5rem !important;
        font-weight:800 !important;
        line-height:1.5 !important;
    }}

    .question-body{{
        color:#1E293B !important;
        margin:0 !important;
        font-size:1.5rem !important;
        line-height:1.8 !important;
        font-weight:800 !important;
    }}

    .main-support-card{{
        background:#F3F0FF !important;
        max-width:720px !important;
        margin:auto !important;
        padding:32px !important;
        border-radius:30px !important;
        box-shadow:0 14px 40px rgba(15, 23, 42, 0.08) !important;
        margin-bottom:30px !important;
    }}

    .category-card{{
        background:#F3F0FF !important;
        border:1px solid #E5E7EB !important;
        border-radius:24px !important;
        padding:24px !important;
        margin-bottom:24px !important;
    }}

    .category-title{{
        font-size:2rem !important;
        font-weight:800 !important;
        color:#111827 !important;
        margin-bottom:18px !important;
    }}

    @keyframes fadeIn{{
        from{{opacity:0; transform:translateY(12px);}}
        to{{opacity:1; transform:translateY(0);}}
    }}
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🎯 Kuesioner Profil Bakat & Minat")
    
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 1
        
    st.progress((st.session_state.current_step - 1) / 4)

    def render_step_header(step, question_text):
        st.markdown(f"""
            <div class='question-header'>
                <div class='step-chip'>Pertanyaan {step} dari 5</div>
                <div class='question-body'>{question_text}</div>
            </div>
        """, unsafe_allow_html=True)

    # ==================== TAHAP 1: MINAT ====================
    if st.session_state.current_step == 1:
        render_step_header(1,  "Bidang apa yang paling membuatmu tertarik dan antusias?")

        create_minat_accordion(minat_dict, 'minat', "Pilih 1 minat terbesarmu!", terjemahan_minat)

        st.markdown("---")

        col1, col2 = st.columns([1,1], gap="large")

        #with col1:
        #    back_btn = st.button(
        #        "Kembali",
        #        key="back_1",
        #        use_container_width=True,
        #        type="secondary"
        #    )

        with col2:
            next_btn = st.button(
                "Selanjutnya",
                key="next_1",
                use_container_width=True,
                type="primary"
            )

        #if back_btn:
        #    st.session_state.page = "home"
        #    st.rerun()

        if next_btn:
            minat_val = get_selected_checkboxes(
                minat_dict,
                'minat'
            )
            if len(minat_val) == 0:
                st.error("⚠️ Pilih minimal 1 minat!")

            elif len(minat_val) > 1:
                st.error("⚠️ Maksimal 1 minat yang dapat dipilih!")

            else:
                st.session_state['minat'] = minat_val[0] if isinstance(minat_val, list) else minat_val
                st.session_state.current_step = 2
                st.rerun()

    # ==================== TAHAP 2: HARD SKILL ====================
    elif st.session_state.current_step == 2:
        render_step_header(2, "Keahlian teknis (Hard Skill) apa yang paling kamu kuasai saat ini?")
        
        #Hasil di halaman sebelumnya untuk debug
        #with st.expander("📊 Debug - Jawaban Sebelumnya"):
        #    st.write(f"**Minat yang dipilih:** {st.session_state.minat}")
        
        create_checkbox_group(
            hard_skill_dict,
            'hard_skill',
            "Pilih keahlian teknismu (Maksimal 2 pilihan)", 
            translation_dict=terjemahan_hard
        )

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            back_btn = st.button(
                "Kembali",
                key="back_2",
                use_container_width=True,
                type="secondary"
            )

        with col2:
            next_btn = st.button(
                "Selanjutnya",
                key="next_2",
                use_container_width=True,
                type="primary"
            )

        if back_btn:
            st.session_state.current_step = 1
            st.rerun()

        if next_btn:
            selected_hard_skill = get_selected_checkboxes(
                hard_skill_dict,
                'hard_skill'
            )

            if len(selected_hard_skill) == 0:
                st.error("⚠️ Pilih minimal 1 keahlian teknis!")

            elif len(selected_hard_skill) > 2:
                st.error("⚠️ Maksimal 2 keahlian teknis yang dapat dipilih!")

            else:
                st.session_state['hard_skill'] = selected_hard_skill
                st.session_state.current_step = 3
                st.rerun()

   # ==================== TAHAP 3: SOFT SKILL ====================
    elif st.session_state.current_step == 3:
        render_step_header(3, "Keterampilan personal (Soft Skill) apa yang paling menonjol dari dirimu?")

        #Hasil di halaman sebelumnya untuk debug
        with st.expander("📊 Debug - Jawaban Sebelumnya"):
            st.write(f"**Minat yang dipilih:** {st.session_state.minat}")
            st.write(f"**Keahlian teknis yang dipilih:** {st.session_state.hard_skill}")

        create_checkbox_group(
            soft_skill_dict,
            'soft_skill',
            "Pilih keterampilan personalmu (Maksimal 2 pilihan)"
        )

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            back_btn = st.button(
                "Kembali",
                key="back_3",
                use_container_width=True,
                type="secondary"
            )

        with col2:
            next_btn = st.button(
                "Selanjutnya",
                key="next_3",
                use_container_width=True,
                type="primary"
            )

        if back_btn:
            st.session_state.current_step = 2
            st.rerun()

        if next_btn:
            selected_soft_skill = get_selected_checkboxes(
                soft_skill_dict,
                'soft_skill'
            )

            if len(selected_soft_skill) == 0:
                st.error("⚠️ Pilih minimal 1 keterampilan personal!")

            elif len(selected_soft_skill) > 2:
                st.error("⚠️ Maksimal 2 keterampilan personal yang dapat dipilih!")

            else:
                st.session_state['soft_skill'] = selected_soft_skill
                st.session_state.current_step = 4
                st.rerun()

    # ==================== TAHAP 4: MAPEL ====================
    elif st.session_state.current_step == 4:
        render_step_header(4, "Mata pelajaran apa yang paling kamu sukai atau selalu mendapat nilai tertinggi?")

        #Hasil di halaman sebelumnya untuk debug
        #with st.expander("📊 Debug - Nilai Sebelumnya"):
        #    st.write(f"**Minat yang dipilih:** {st.session_state.minat}")
        #   st.write(f"**Keahlian teknis yang dipilih:** {st.session_state.hard_skill}")
        #    st.write(f"**Keterampilan personal yang dipilih:** {st.session_state.soft_skill}")
            
        create_checkbox_group(
            mapel_dict,
            'mapel',
            "Pilih mata pelajaran favoritmu! (Maksimal 3 pilihan)", 
            translation_dict=terjemahan_mapel
        )

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            back_btn = st.button(
                "Kembali",
                key="back_4",
                use_container_width=True,
                type="secondary"
            )

        with col2:
            next_btn = st.button(
                "Selanjutnya",
                key="next_4",
                use_container_width=True,
                type="primary"
            )

        if back_btn:
            st.session_state.current_step = 3
            st.rerun()

        if next_btn:
            selected_mapel = get_selected_checkboxes(
                mapel_dict,
                'mapel'
            )

            if len(selected_mapel) == 0:
                st.error("⚠️ Pilih minimal 1 pelajaran!")

            elif len(selected_mapel) > 3:
                st.error("⚠️ Maksimal 3 pelajaran yang dapat dipilih!")

            else:
                st.session_state['mapel'] = selected_mapel
                st.session_state.current_step = 5
                st.rerun()

    # ==================== TAHAP 5: PENDUKUNG (RULE-BASED) ====================
    elif st.session_state.current_step == 5:
        render_step_header(
            5,
            "Lengkapi profil keseharianmu!"
        )

        #Hasil di halaman sebelumnya untuk debug
        #with st.expander("📊 Debug - Jawaban Sebelumnya"):
        #    st.write(f"**Minat yang dipilih:** {st.session_state.minat}")
        #    st.write(f"**Keahlian teknis yang dipilih:** {st.session_state.hard_skill}")
        #    st.write(f"**Keterampilan personal yang dipilih:** {st.session_state.soft_skill}")
        #    st.write(f"**Pelajaran favorit yang dipilih:** {st.session_state.mapel}")

        # ================= JURUSAN =================
        with st.expander("**Jurusan SMA/SMK**", expanded=True):
            create_single_checkbox_group(
                jurusan_dict,
                "jurusan_sekolah",
                detail_jurusan=detail_jurusan
            )

        # ================= KEPRIBADIAN =================
        with st.expander("**Kepribadian**", expanded=False):
            create_single_checkbox_group(
                personality_dict,
                "personality"
            )

        # ================= HOBI =================
        with st.expander("**Hobi**", expanded=False):
            create_single_checkbox_group(
                hobi_dict,
                "hobi"
            )

        # ================= EKSKUL =================
        with st.expander("**Ekstrakurikuler**", expanded=False):
            create_single_checkbox_group(
                ekskul_dict,
                "ekskul"
            )

        st.markdown("---")

        col1, col2 = st.columns([1,1], gap="large")

        with col1:
            back_btn = st.button(
                "Kembali",
                key="back_5",
                use_container_width=True,
                type="secondary"
            )

        with col2:
            result_btn = st.button(
                "Lihat Hasil Analisis",
                key="result_5",
                use_container_width=True,
                type="primary"
            )

        if back_btn:
            st.session_state.current_step = 4
            st.rerun()

        if result_btn:
            jurusan = st.session_state.get("jurusan_sekolah", [])
            personality = st.session_state.get("personality", [])
            hobi = st.session_state.get("hobi", [])
            ekskul = st.session_state.get("ekskul", [])

            # 1. Cek apakah ada kategori yang sama sekali belum dipilih (list kosong)
            if not jurusan or not personality or not hobi or not ekskul:
                st.warning("⚠️ Eits, tunggu dulu! Pastikan kamu sudah memilih Jurusan, Kepribadian, Hobi, dan Ekstrakurikuler ya.")
            
            # 2. Cek apakah ada kategori yang dipilih lebih dari satu (isi list > 1)
            elif len(jurusan) > 1 or len(personality) > 1 or len(hobi) > 1 or len(ekskul) > 1:
                st.warning("⚠️ Wah, pilihannya kebanyakan! Tolong pilih maksimal SATU saja untuk setiap kategori ya.")
            
            # 3. Jika aman (tepat 1 pilihan di setiap kategori)
            else:
                st.session_state.page = "result"
                st.rerun()