import streamlit as st
from views.kamus import (minat_dict, hard_skill_dict, soft_skill_dict, mapel_dict,
                         jurusan_dict, ekskul_dict, personality_dict, hobi_dict,
                         create_minat_accordion, create_checkbox_group,
                         create_radio_by_category, get_selected_checkboxes)

def show_question():
    st.title("🎯 Kuesioner Profil Bakat & Minat")
    
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 1
        
    st.progress((st.session_state.current_step - 1) / 4)

    # ==================== TAHAP 1: MINAT ====================
    if st.session_state.current_step == 1:
        st.caption("Pertanyaan 1 dari 5 (Fitur Utama)")
        st.subheader("Bidang apa yang paling membuatmu tertarik dan antusias?")
        
        create_minat_accordion(minat_dict, 'minat', "Pilih minat terbesarmu:")
        
        st.markdown("---")
        col1, col2 = st.columns(2)
        if col1.button("⬅️ Kembali"):
            st.session_state.page = 'home'
            st.rerun()
        if col2.button("Selanjutnya ➡️", use_container_width=True):
            if not st.session_state.get('minat'):
                st.error("⚠️ Pilih salah satu minat sebelum melanjutkan!")
            else:
                st.session_state.current_step = 2
                st.rerun()

    # ==================== TAHAP 2: HARD SKILL ====================
    elif st.session_state.current_step == 2:
        st.caption("Pertanyaan 2 dari 5 (Fitur Utama)")
        st.subheader("Keahlian teknis (Hard Skill) apa yang paling kamu kuasai saat ini?")
        
        with st.form("form_q2"):
            create_checkbox_group(hard_skill_dict, 'hard_skill', "Pilih keahlian teknismu")
            submitted_q2 = st.form_submit_button("Selanjutnya ➡️")
            
        if submitted_q2:
            selected_hard_skill = get_selected_checkboxes(hard_skill_dict, 'hard_skill')
            if len(selected_hard_skill) == 0:
                st.error("⚠️ Pilih minimal 1 keahlian teknis!")
            elif len(selected_hard_skill) > 2:
                st.error("⚠️ Maksimal 2 keahlian teknis yang dapat dipilih!")
            else:
                st.session_state['hard_skill'] = selected_hard_skill
                st.session_state.current_step = 3
                st.rerun()
                
        if st.button("⬅️ Kembali"):
            st.session_state.current_step = 1
            st.rerun()

    # ==================== TAHAP 3: SOFT SKILL ====================
    elif st.session_state.current_step == 3:
        st.caption("Pertanyaan 3 dari 5 (Fitur Utama)")
        st.subheader("Keterampilan personal (Soft Skill) apa yang paling menonjol dari dirimu?")
        
        with st.form("form_q3"):
            create_checkbox_group(soft_skill_dict, 'soft_skill', "Pilih keterampilan personalmu")
            submitted_q3 = st.form_submit_button("Selanjutnya ➡️")
            
        if submitted_q3:
            selected_soft_skill = get_selected_checkboxes(soft_skill_dict, 'soft_skill')
            if len(selected_soft_skill) == 0:
                st.error("⚠️ Pilih minimal 1 keterampilan personal!")
            elif len(selected_soft_skill) > 2:
                st.error("⚠️ Maksimal 2 keterampilan personal yang dapat dipilih!")
            else:
                st.session_state['soft_skill'] = selected_soft_skill
                st.session_state.current_step = 4
                st.rerun()
                
        if st.button("⬅️ Kembali"):
            st.session_state.current_step = 2
            st.rerun()

    # ==================== TAHAP 4: MAPEL ====================
    elif st.session_state.current_step == 4:
        st.caption("Pertanyaan 4 dari 5 (Fitur Utama)")
        st.subheader("Mata pelajaran apa yang paling kamu sukai atau dapatkan nilai tertinggi?")
        
        with st.form("form_q4"):
            create_radio_by_category(mapel_dict, 'mapel', "Pilih mata pelajaran favoritmu:")
            submitted_q4 = st.form_submit_button("Selanjutnya ➡️")
            
        if submitted_q4:
            st.session_state.current_step = 5
            st.rerun()
            
        if st.button("⬅️ Kembali"):
            st.session_state.current_step = 3
            st.rerun()

    # ==================== TAHAP 5: PENDUKUNG (RULE-BASED) ====================
    elif st.session_state.current_step == 5:
        st.caption("Pertanyaan Terakhir (Fitur Pendukung)")
        st.subheader("Lengkapi profil keseharianmu!")
        
        with st.form("form_q_pendukung"):
            jurusan_list = list(jurusan_dict.keys())
            jurusan_idx = jurusan_list.index(st.session_state.jurusan_sekolah) if st.session_state.jurusan_sekolah in jurusan_list else 0
            st.radio("Jurusan saat SMA/SMK:", jurusan_list, index=jurusan_idx, format_func=lambda x: x.title(), key='jurusan_sekolah')
            
            personality_list = list(personality_dict.keys())
            pers_idx = personality_list.index(st.session_state.personality) if st.session_state.personality in personality_list else 0
            st.radio("Kepribadian (Personality):", personality_list, index=pers_idx, format_func=lambda x: x.title(), key='personality')
            
            hobi_list = list(hobi_dict.keys())
            hobi_idx = hobi_list.index(st.session_state.hobi) if st.session_state.hobi in hobi_list else 0
            st.radio("Hobi Utama:", hobi_list, index=hobi_idx, format_func=lambda x: x.title(), key='hobi')
            
            ekskul_list = list(ekskul_dict.keys())
            eksk_idx = ekskul_list.index(st.session_state.ekskul) if st.session_state.ekskul in ekskul_list else 0
            st.radio("Ekstrakurikuler:", ekskul_list, index=eksk_idx, format_func=lambda x: x.title(), key='ekskul')
            
            submitted_q5 = st.form_submit_button("Lihat Hasil Analisis 🚀")
            
        if submitted_q5:
            st.session_state.page = 'result'
            st.rerun()
            
        if st.button("⬅️ Kembali"):
            st.session_state.current_step = 4
            st.rerun()