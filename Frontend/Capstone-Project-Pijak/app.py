import streamlit as st
import pickle

# ==========================================
# 1. KONFIGURASI & LOAD MODEL
# ==========git add app.py================================
st.set_page_config(page_title="Pijak Karier", page_icon="🎓", layout="centered")

@st.cache_resource
def load_models():
    try:
        with open('model_pijak.pkl', 'rb') as file:
            model = pickle.load(file)
        with open('tfidf_pijak.pkl', 'rb') as file:
            tfidf = pickle.load(file)
        with open('label_encoder.pkl', 'rb') as file:
            le = pickle.load(file)
        return model, tfidf, le
    except Exception as e:
        return None, None, None

model, tfidf, le = load_models()

# ==========================================
# 2. STATE MANAGEMENT (Inisialisasi)
# ==========================================
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Inisialisasi semua kunci session state agar selalu tersedia
state_keys = {
    'minat': '', 'hard_skill': [], 'soft_skill': [], 'mapel': '',
    'jurusan_sekolah': '', 'personality': '', 'hobi': '', 'ekskul': ''
}
for key in state_keys:
    if key not in st.session_state:
        st.session_state[key] = state_keys[key]

def set_page(page_name):
    st.session_state.page = page_name

def reset_state():
    """Reset semua pilihan dan kembali ke halaman awal."""
    for key, default_value in state_keys.items():
        st.session_state[key] = default_value

    # Hapus checkbox widget state yang bisa tersisa dari sesi sebelumnya.
    for key in ['hard_skill', 'soft_skill']:
        items_dict = hard_skill_dict if key == 'hard_skill' else soft_skill_dict
        for option in items_dict.keys():
            widget_key = f"{key}_{option}"
            if widget_key in st.session_state:
                del st.session_state[widget_key]

    st.session_state.page = 'home'

def create_radio_by_category(items_dict, session_key, label_text):
    """
    Menampilkan radio button untuk pilihan dari dictionary.
    Menyimpan pilihan ke session state tanpa konflik widget key.
    """
    options = list(items_dict.keys())
    current_value = st.session_state.get(session_key, '')
    index = options.index(current_value) if current_value in options else 0
    selected = st.radio(
        label_text,
        options,
        index=index,
        format_func=lambda x: x.title()
    )
    st.session_state[session_key] = selected
    return selected

def create_grouped_radio_by_category(items_dict, session_key, label_text):
    """
    Menampilkan dua-langkah grouped selector:
    1) Pilih kategori (bidang)
    2) Pilih opsi spesifik dalam kategori tersebut

    Ini membuat tampilan seperti "section" untuk setiap kategori.
    """
    # Susun kategori berdasarkan urutan kemunculan pada items_dict
    categories = []
    for k, v in items_dict.items():
        if v not in categories:
            categories.append(v)

    # Tentukan kategori awal berdasarkan nilai yang tersimpan
    current_value = st.session_state.get(session_key, '')
    initial_category = None
    if current_value:
        initial_category = items_dict.get(current_value)
    if initial_category not in categories:
        initial_category = categories[0] if categories else None

    # Pilih kategori
    selected_category = st.selectbox("Pilih Bidang (Kategori):", categories, index=categories.index(initial_category) if initial_category in categories else 0, format_func=lambda x: x)

    # Kumpulkan opsi untuk kategori yang dipilih
    options = [k for k, v in items_dict.items() if v == selected_category]
    # Tentukan index awal untuk opsi jika sebelumnya sudah memilih
    index = 0
    if current_value in options:
        index = options.index(current_value)

    selected = st.radio(label_text, options, index=index, format_func=lambda x: x.title())
    st.session_state[session_key] = selected
    return selected

def create_minat_accordion(items_dict, session_key, label_text):
    """
    Menampilkan setiap kategori minat sebagai accordion (expander) terpisah.
    Di dalam setiap accordion, opsi kategori ditampilkan sebagai tombol,
    sehingga hanya satu nilai global disimpan di session state.
    """
    st.write(f"**{label_text}**")

    categories = []
    cat_items = {}
    for opt, cat in items_dict.items():
        if cat not in cat_items:
            cat_items[cat] = []
            categories.append(cat)
        cat_items[cat].append(opt)

    current_value = st.session_state.get(session_key, "")

    for cat in categories:
        expanded = current_value in cat_items[cat]
        with st.expander(cat.upper(), expanded=expanded):
            cols = st.columns(2)
            for i, opt in enumerate(cat_items[cat]):
                col = cols[i % 2]
                label = opt.title()
                if current_value == opt:
                    label = f"{label} ✅"
                if col.button(label, key=f"{session_key}_{cat}_{opt}"):
                    st.session_state[session_key] = opt

    return st.session_state.get(session_key, "")

def create_grouped_buttons_with_headers(items_dict, session_key, label_text):
    """
    Tampilkan semua opsi dengan header kategori (kapital) di atasnya.
    Opsi ditampilkan sebagai tombol; tombol bukan bagian dari radio,
    jadi klik tombol akan langsung menyimpan pilihan ke session state.
    """
    # Bangun map kategori -> list opsi
    cat_items = {}
    for opt, cat in items_dict.items():
        cat_items.setdefault(cat, []).append(opt)

    st.write(f"**{label_text}**")
    for cat, items in cat_items.items():
        st.markdown(f"**{cat.upper()}**")
        # Tampilkan opsi sebagai tombol dalam dua kolom
        cols = st.columns(2)
        for i, opt in enumerate(items):
            col = cols[i % 2]
            label = opt.title()
            if st.session_state.get(session_key) == opt:
                label = f"{label} ✅"
            if col.button(label, key=f"{session_key}_btn_{opt}"):
                st.session_state[session_key] = opt
                # UI akan rerun otomatis di Streamlit setelah klik tombol

def simpan_checkbox_dan_lanjut(target_page, items_dict, session_key):
    """
    Fungsi ini akan menangkap semua checkbox yang dicentang sebelum pindah halaman,
    lalu menyimpannya dengan aman ke dalam st.session_state sebagai list.
    """
    selected = []
    for option in items_dict.keys():
        widget_key = f"{session_key}_{option}"
        # Jika checkbox dicentang (True), masukkan teksnya ke dalam list
        if st.session_state.get(widget_key, False):
            selected.append(option)
            
    st.session_state[session_key] = selected
    st.session_state.page = target_page
    st.rerun()

def get_selected_checkboxes(items_dict, session_key):
    selected = []
    for option in items_dict.keys():
        widget_key = f"{session_key}_{option}"
        if st.session_state.get(widget_key, option in st.session_state.get(session_key, [])):
            selected.append(option)
    return selected


def get_jurusan_populer_text(bidang):
    if bidang == "Komputer dan Teknologi":
        return "Teknik Informatika<br>Sistem Informasi<br>Ilmu Komputer<br>Teknologi Informasi<br>Sistem Komputer"
    elif bidang == "Teknik":
        return "Teknik Industri<br>Teknik Sipil<br>Teknik Mesin<br>Teknik Elektro<br>Teknik Kimia"
    elif bidang == "Kesehatan":
        return "Kedokteran<br>Keperawatan<br>Farmasi<br>Kesehatan Masyarakat<br>Gizi"
    elif bidang == "Ekonomi dan Bisnis":
        return "Akuntansi<br>Manajemen<br>Bisnis Digital<br>Kewirausahaan<br>Ekonomi Pembangunan<br>"
    elif bidang == "Pendidikan":
        return "PGSD<br>PGPAUD<br>Pendidikan Bahasa Inggris<br>Pendidikan Matematika<br>Pendidikan Bahasa Indonesia"
    elif bidang == "Seni":
        return "DKV<br>Seni Rupa<br>Desain Produk<br>Film<br>Fotografi"
    elif bidang == "Sosial dan Humaniora":
        return "Hukum<br>Psikologi<br>Ilmu Komunikasi<br>Hubungan Internasional<br>Administrasi Publik"
    elif bidang == "Pertanian":
        return "Agribisnis<br>Agroteknologi<br>Teknologi Pangan<br>Peternakan<br>Kehutanan"
    elif bidang == "Sains dan MIPA":
        return "Matematika<br>Statistika<br>Fisika<br>Kimia<br>Biologi"
    else:
        return "Agribisnis<br>Agroteknologi<br>Teknologi Pangan<br>Peternakan<br>Kehutanan"


def create_checkbox_group(items_dict, session_key, label_text):
    """
    Menampilkan deretan checkbox dalam bentuk 2 kolom agar rapi dan ringkas.
    Membatasi maksimal 2 pilihan yang dapat dipilih.
    """
    st.write(f"**{label_text}** (Maksimal 2 pilihan)")
    options = list(items_dict.keys())
    
    # Hitung berapa banyak checkbox yang sudah dicentang saat ini
    checked_count = sum(
        1
        for option in options
        if st.session_state.get(f"{session_key}_{option}", option in st.session_state.get(session_key, []))
    )
    
    # Membagi menjadi 2 kolom agar "terlihat dalam satu pandangan mata"
    cols = st.columns(2) 
    
    for i, option in enumerate(options):
        widget_key = f"{session_key}_{option}"
        is_checked = st.session_state.get(widget_key, option in st.session_state.get(session_key, []))
        
        # Disable checkbox jika sudah 2 pilihan dan opsi ini belum dicentang
        disabled = checked_count >= 2 and not is_checked
        
        with cols[i % 2]:
            st.checkbox(option.title(), value=is_checked, key=widget_key, disabled=disabled)

# ==========================================
# 2. KAMUS DATA (DICTIONARY)
# ==========================================

# --- A. FITUR UTAMA (UNTUK MACHINE LEARNING) ---
minat_dict = {
    "coding": "Komputer dan Teknologi", "programming": "Komputer dan Teknologi", "artificial intelligence": "Komputer dan Teknologi", "machine learning": "Komputer dan Teknologi", "web development": "Komputer dan Teknologi", "software": "Komputer dan Teknologi", "cyber security": "Komputer dan Teknologi", "data science": "Komputer dan Teknologi", "game development": "Komputer dan Teknologi", "technology": "Komputer dan Teknologi", "information technology": "Komputer dan Teknologi", "it": "Komputer dan Teknologi", "cloud computing": "Komputer dan Teknologi", "data analytics": "Komputer dan Teknologi", "data scientist": "Komputer dan Teknologi", "web designing": "Komputer dan Teknologi", "blockchain": "Komputer dan Teknologi", "software developer": "Komputer dan Teknologi", "software engineer": "Komputer dan Teknologi",
    "robotics": "Teknik", "mechanics": "Teknik", "electronics": "Teknik", "automobile": "Teknik", "construction": "Teknik", "engineering": "Teknik", "oil and gas": "Teknik", "project management": "Teknik", "construction manegement": "Teknik", "infrastructure": "Teknik",
    "doctor": "Kesehatan", "medical": "Kesehatan", "pharmacy": "Kesehatan", "nutrition": "Kesehatan", "healthcare": "Kesehatan", "understand human body": "Kesehatan", "medicine": "Kesehatan",
    "business": "Ekonomi dan Bisnis", "finance": "Ekonomi dan Bisnis", "marketing": "Ekonomi dan Bisnis", "entrepreneurship": "Ekonomi dan Bisnis", "accounting": "Ekonomi dan Bisnis", "financial analysis": "Ekonomi dan Bisnis", "sales/marketing": "Ekonomi dan Bisnis", "trading": "Ekonomi dan Bisnis", "market reserach": "Ekonomi dan Bisnis", "business analytics": "Ekonomi dan Bisnis", "supply chain analysis": "Ekonomi dan Bisnis",
    "teaching": "Pendidikan", "education": "Pendidikan", "govt. job": "Pendidikan", "government jobs": "Pendidikan",
    "music": "Seni", "drawing": "Seni", "photography": "Seni", "animation": "Seni", "design": "Seni", "video editing": "Seni", "home interior design": "Seni",
    "psychology": "Sosial dan Humaniora", "law": "Sosial dan Humaniora", "journalism": "Sosial dan Humaniora", "communication": "Sosial dan Humaniora", "politics": "Sosial dan Humaniora",
    "farming": "Pertanian", "agriculture": "Pertanian", "livestock": "Pertanian", "plant cultivation": "Pertanian", "gardening": "Pertanian",
    "mathematics": "Sains dan MIPA", "physics": "Sains dan MIPA", "chemistry": "Sains dan MIPA", "biology": "Sains dan MIPA", "research": "Sains dan MIPA", "science": "Sains dan MIPA"
}

hard_skill_dict = {
    "programming": "Komputer dan Teknologi", "coding": "Komputer dan Teknologi", "python": "Komputer dan Teknologi", "java": "Komputer dan Teknologi", "c++": "Komputer dan Teknologi", "web development": "Komputer dan Teknologi", "software development": "Komputer dan Teknologi", "machine learning": "Komputer dan Teknologi", "artificial intelligence": "Komputer dan Teknologi", "database": "Komputer dan Teknologi", "data analysis": "Komputer dan Teknologi", "networking": "Komputer dan Teknologi", "cyber security": "Komputer dan Teknologi",
    "autocad": "Teknik", "machining": "Teknik", "mechanical repair": "Teknik", "electrical wiring": "Teknik", "electronics": "Teknik", "robotics": "Teknik", "circuit design": "Teknik", "engineering drawing": "Teknik", "civil": "Teknik",
    "patient care": "Kesehatan", "medical knowledge": "Kesehatan", "clinical analysis": "Kesehatan", "pharmaceutical knowledge": "Kesehatan", "nutrition analysis": "Kesehatan",
    "accounting": "Ekonomi dan Bisnis", "finance": "Ekonomi dan Bisnis", "marketing": "Ekonomi dan Bisnis", "sales": "Ekonomi dan Bisnis", "business analysis": "Ekonomi dan Bisnis", "bookkeeping": "Ekonomi dan Bisnis", "management": "Ekonomi dan Bisnis",
    "teaching": "Pendidikan", "lesson planning": "Pendidikan", "mentoring": "Pendidikan", "curriculum design": "Pendidikan",
    "graphic design": "Seni", "animation": "Seni", "video editing": "Seni", "drawing": "Seni", "photography": "Seni", "music production": "Seni", "fashion design": "Seni",
    "public speaking": "Sosial dan Humaniora", "journalism": "Sosial dan Humaniora", "writing": "Sosial dan Humaniora", "legal analysis": "Sosial dan Humaniora", "communication": "Sosial dan Humaniora", "foreign language": "Sosial dan Humaniora", "negotiation": "Sosial dan Humaniora",
    "farming": "Pertanian", "plant cultivation": "Pertanian", "soil analysis": "Pertanian", "agricultural technology": "Pertanian", "livestock management": "Pertanian",
    "mathematics": "Sains dan MIPA", "statistics": "Sains dan MIPA", "research": "Sains dan MIPA", "laboratory analysis": "Sains dan MIPA", "scientific analysis": "Sains dan MIPA", "physics calculation": "Sains dan MIPA", "chemical analysis": "Sains dan MIPA"
}

soft_skill_dict = {
    "problem solving": "Problem Solving", "analytical thinking": "Analytical Thinking", "creativity": "Creativity", "communication": "Communication", "leadership": "Leadership", "teamwork": "Teamwork", "time management": "Time Management", "adaptability": "Adaptability", "responsibility": "Responsibility", "public speaking": "Public Speaking", "empathy": "Empathy", "accuracy": "Accuracy"
}

mapel_dict = {
    "computer science engineering": "Komputer dan Teknologi", "computer science": "Komputer dan Teknologi", "computer applications": "Komputer dan Teknologi", "information technology": "Komputer dan Teknologi", "programming": "Komputer dan Teknologi", "coding": "Komputer dan Teknologi", "software development": "Komputer dan Teknologi",
    "mechanical engineering": "Teknik", "civil engineering": "Teknik", "electrical engineering": "Teknik", "electrical and electronics engineering": "Teknik", "electronics and communication engineering": "Teknik", "automobile engineering": "Teknik", "chemical engineering": "Teknik", "instrumentation engineering": "Teknik", "structural engineeeing": "Teknik", "engineering": "Teknik", "aeronautical": "Teknik",
    "pharmacy": "Kesehatan", "dental surgeon": "Kesehatan", "dietician": "Kesehatan", "hospital administration": "Kesehatan",
    "commerce": "Ekonomi dan Bisnis", "accountancy": "Ekonomi dan Bisnis", "finance": "Ekonomi dan Bisnis", "business administration": "Ekonomi dan Bisnis", "marketing": "Ekonomi dan Bisnis", "sales & marketing": "Ekonomi dan Bisnis", "accounting": "Ekonomi dan Bisnis", "economics": "Ekonomi dan Bisnis", "business": "Ekonomi dan Bisnis",
    "education": "Pendidikan", "general studies": "Pendidikan", "Bahasa Indonesia": "Pendidikan",
    "Seni Budaya": "Seni", "Desain Grafis": "Seni", "Multimedia": "Seni", "animation": "Seni", "animation & visual effects": "Seni", "fashion designing": "Seni", "interior design": "Seni", "design": "Seni", "advertising": "Seni", "autocad": "Seni",
    "psychology": "Sosial dan Humaniora", "history": "Sosial dan Humaniora", "political science": "Sosial dan Humaniora", "law": "Sosial dan Humaniora", "journalism": "Sosial dan Humaniora", "english": "Sosial dan Humaniora", "sociology": "Sosial dan Humaniora", "literature": "Sosial dan Humaniora",
    "agriculture": "Pertanian", "agriculture engineering": "Pertanian", "agriculture biotechnalogy": "Pertanian",
    "mathematics": "Sains dan MIPA", "physics": "Sains dan MIPA", "chemistry": "Sains dan MIPA", "statistics": "Sains dan MIPA", "science": "Sains dan MIPA", "biotechnology": "Sains dan MIPA", "bio technology": "Sains dan MIPA", "botany": "Sains dan MIPA", "microbiology": "Sains dan MIPA"
}

# --- B. FITUR PENDUKUNG (UNTUK RULE-BASED) ---
jurusan_dict = {
    "IPA": ["Sains dan MIPA", "Kesehatan", "Teknik"], "IPS": ["Ekonomi dan Bisnis", "Sosial dan Humaniora"], "Bahasa": ["Pendidikan", "Sosial dan Humaniora", "Seni"],
    "RPL": ["Komputer dan Teknologi"], "TKJ": ["Komputer dan Teknologi"], "Multimedia": ["Komputer dan Teknologi", "Seni"],
    "Akuntansi": ["Ekonomi dan Bisnis"], "AKL": ["Ekonomi dan Bisnis"], "Perbankan": ["Ekonomi dan Bisnis"],
    "TKR": ["Teknik"], "TBSM": ["Teknik"], "Teknik Mesin": ["Teknik"], "Teknik Elektro": ["Teknik"], "Farmasi": ["Kesehatan"], "Perhotelan": ["Ekonomi dan Bisnis", "Sosial dan Humaniora"]
}

ekskul_dict = {
    "programing club": ["Komputer dan Teknologi"], "PMR": ["Kesehatan"], "oLahraga": ["Kesehatan"], "bela diri": ["Kesehatan"], "kewirausahaan": ["Ekonomi dan Bisnis"], "tutor": ["Pendidikan"],
    "teater": ["Seni"], "paduan suara": ["Seni"], "kesenian": ["Seni"], "desain grafis": ["Seni"], "fotografi": ["Seni"], "jurnalistik": ["Sosial dan Humaniora"], "debat": ["Sosial dan Humaniora"], "OSIS": ["Sosial dan Humaniora"],
    "tani sekolah": ["Pertanian"], "KIR": ["Sains dan MIPA", "Komputer dan Teknologi"], "robotik": ["Komputer dan Teknologi", "Teknik"], "english club": ["Pendidikan", "Sosial dan Humaniora"], "pramuka": ["Pendidikan", "Sosial dan Humaniora"], "paskibra": ["Pendidikan", "Sosial dan Humaniora"]
}

personality_dict = {
    "Introvert": ["Komputer dan Teknologi", "Sains dan MIPA", "Seni"],
    "Ambivert": ["Komputer dan Teknologi", "Teknik", "Ekonomi dan Bisnis", "Pendidikan", "Sosial dan Humaniora"],
    "Extrovert": ["Ekonomi dan Bisnis", "Pendidikan", "Sosial dan Humaniora", "Kesehatan"]
}

hobi_dict = {
    "bermain game": ["Komputer dan Teknologi"], "pemograman": ["Komputer dan Teknologi"], "blogging": ["Komputer dan Teknologi", "Sosial dan Humaniora"],
    "merakit": ["Teknik"], "catur": ["Teknik"], "puzzle": ["Teknik"], "robotik": ["Komputer dan Teknologi", "Teknik"], "modifikasi": ["Teknik"],
    "olahraga": ["Kesehatan"], "bisnis": ["Ekonomi dan Bisnis"],
    "mengajar": ["Pendidikan"], "belajar": ["Pendidikan"], "belajar bahasa": ["Pendidikan"], "membaca buku": ["Pendidikan"],
    "menggambar/melukis": ["Seni"], "musik": ["Seni"], "menari": ["Seni"], "fotografi": ["Seni"], "editing video": ["Seni"], "animasi": ["Seni"], "menulis cerita": ["Seni", "Sosial dan Humaniora"], "bermain alat musik": ["Seni"],
    "menulis": ["Sosial dan Humaniora"], "travelling": ["Sosial dan Humaniora"], "menonton": ["Sosial dan Humaniora"], "debat": ["Sosial dan Humaniora"], "organisasi": ["Sosial dan Humaniora"],
    "berkebun": ["Pertanian"], "menanam": ["Pertanian"], "bertani": ["Pertanian"],
    "eksperimen": ["Sains dan MIPA"], "membaca sains": ["Sains dan MIPA"], "meneliti": ["Sains dan MIPA"]
}

# ==========================================
# 4. TAMPILAN HALAMAN (PAGES)
# ==========================================

if st.session_state.page == 'home':
    st.title("🎓 Pijak Karier")
    st.subheader("Kenali Potensi Dirimu, Temukan Karier Impianmu!")
    st.write("Selamat datang di Pijak Karier! Tes ini dirancang khusus untuk siswa SMA dan lulusan gap year. Melalui beberapa pertanyaan sederhana mengenai minat, keahlian, dan kepribadianmu, teknologi AI kami akan membantu merekomendasikan bidang studi dan karier yang paling tepat untukmu.")
    st.info("⏱️ Tes ini hanya membutuhkan waktu sekitar 2-3 menit.")
    st.write("---")
    st.button("Mulai Tes Sekarang ✨", on_click=set_page, args=('q1',), use_container_width=True)

elif st.session_state.page == 'q1':
    st.progress(20)
    st.caption("Pertanyaan 1 dari 5 (Fitur Utama)")
    st.subheader("Bidang apa yang paling membuatmu tertarik dan antusias?")
    create_minat_accordion(minat_dict, 'minat', "Pilih minat terbesarmu:")
    if st.button("Selanjutnya ➡️"):
        if not st.session_state.get('minat'):
            st.error("⚠️ Pilih salah satu minat sebelum melanjutkan!")
        else:
            set_page('q2')
            st.rerun()
    if st.button("⬅️ Kembali"):
        set_page('home')
        st.rerun()

elif st.session_state.page == 'q2':
    st.progress(40)
    st.caption("Pertanyaan 2 dari 5 (Fitur Utama)")
    with st.expander("📊 Debug - Nilai Sebelumnya"):
        st.write(f"**Minat yang dipilih:** {st.session_state.minat}")
    st.subheader("Keahlian teknis (Hard Skill) apa yang paling kamu kuasai saat ini?")
    with st.form("form_q2"):
        create_checkbox_group(hard_skill_dict, 'hard_skill', "Pilih keahlian teknismu")
        submitted_q2 = st.form_submit_button("Selanjutnya ➡️")
    if submitted_q2:
        selected_hard_skill = get_selected_checkboxes(hard_skill_dict, 'hard_skill')
        hard_skill_count = len(selected_hard_skill)
        if hard_skill_count == 0:
            st.error("⚠️ Pilih minimal 1 keahlian teknis!")
        elif hard_skill_count > 2:
            st.error("⚠️ Maksimal 2 keahlian teknis yang dapat dipilih!")
        else:
            st.session_state['hard_skill'] = selected_hard_skill
            simpan_checkbox_dan_lanjut('q3', hard_skill_dict, 'hard_skill')
    if st.button("⬅️ Kembali"):
        set_page('q1')
        st.rerun()

elif st.session_state.page == 'q3':
    st.progress(60)
    st.caption("Pertanyaan 3 dari 5 (Fitur Utama)")
    with st.expander("📊 Debug - Nilai Sebelumnya"):
        st.write(f"**Minat:** {st.session_state.minat}")
        st.write(f"**Hard Skill:** {st.session_state.hard_skill}")
    st.subheader("Keterampilan personal (Soft Skill) apa yang paling menonjol dari dirimu?")
    with st.form("form_q3"):
        create_checkbox_group(soft_skill_dict, 'soft_skill', "Pilih keterampilan personalmu")
        submitted_q3 = st.form_submit_button("Selanjutnya ➡️")
    if submitted_q3:
        selected_soft_skill = get_selected_checkboxes(soft_skill_dict, 'soft_skill')
        soft_skill_count = len(selected_soft_skill)
        if soft_skill_count == 0:
            st.error("⚠️ Pilih minimal 1 keterampilan personal!")
        elif soft_skill_count > 2:
            st.error("⚠️ Maksimal 2 keterampilan personal yang dapat dipilih!")
        else:
            st.session_state['soft_skill'] = selected_soft_skill
            simpan_checkbox_dan_lanjut('q4', soft_skill_dict, 'soft_skill')
    if st.button("⬅️ Kembali"):
        set_page('q2')
        st.rerun()

elif st.session_state.page == 'q4':
    st.progress(80)
    st.caption("Pertanyaan 4 dari 5 (Fitur Utama)")
    with st.expander("📊 Debug - Nilai Sebelumnya"):
        st.write(f"**Minat:** {st.session_state.minat}")
        st.write(f"**Hard Skill:** {st.session_state.hard_skill}")
        st.write(f"**Soft Skill:** {st.session_state.soft_skill}")
    st.subheader("Mata pelajaran apa yang paling kamu sukai atau dapatkan nilai tertinggi?")
    with st.form("form_q4"):
        create_radio_by_category(mapel_dict, 'mapel', "Pilih mata pelajaran favoritmu:")
        submitted_q4 = st.form_submit_button("Selanjutnya ➡️")
    if submitted_q4:
        set_page('q_pendukung')
        st.rerun()
    if st.button("⬅️ Kembali"):
        set_page('q3')
        st.rerun()

elif st.session_state.page == 'q_pendukung':
    st.progress(100)
    st.caption("Pertanyaan Terakhir (Fitur Pendukung)")
    with st.expander("📊 Debug - Semua Nilai yang Tersimpan"):
        st.write(f"**Minat:** {st.session_state.minat}")
        st.write(f"**Hard Skill:** {st.session_state.hard_skill}")
        st.write(f"**Soft Skill:** {st.session_state.soft_skill}")
        st.write(f"**Mapel:** {st.session_state.mapel}")
    st.subheader("Lengkapi profil keseharianmu!")
    
    with st.form("form_q_pendukung"):
        jurusan_list = list(jurusan_dict.keys())
        jurusan_index = jurusan_list.index(st.session_state.jurusan_sekolah) if st.session_state.jurusan_sekolah in jurusan_list else 0
        st.radio("Jurusan saat SMA/SMK:", jurusan_list, index=jurusan_index, format_func=lambda x: x.title(), key='jurusan_sekolah')
        
        personality_list = list(personality_dict.keys())
        personality_index = personality_list.index(st.session_state.personality) if st.session_state.personality in personality_list else 0
        st.radio("Kepribadian (Personality):", personality_list, index=personality_index, format_func=lambda x: x.title(), key='personality')
        
        hobi_list = list(hobi_dict.keys())
        hobi_index = hobi_list.index(st.session_state.hobi) if st.session_state.hobi in hobi_list else 0
        st.radio("Hobi Utama:", hobi_list, index=hobi_index, format_func=lambda x: x.title(), key='hobi')
        
        ekskul_list = list(ekskul_dict.keys())
        ekskul_index = ekskul_list.index(st.session_state.ekskul) if st.session_state.ekskul in ekskul_list else 0
        st.radio("Ekstrakurikuler:", ekskul_list, index=ekskul_index, format_func=lambda x: x.title(), key='ekskul')
        
        st.form_submit_button("Lihat Hasil Analisis 🚀", on_click=set_page, args=('result',))
    if st.button("⬅️ Kembali"):
        set_page('q4')
        st.rerun()

elif st.session_state.page == 'result':
    st.title("🎉 Hasil Rekomendasi Kamu")
    
    with st.expander("📊 Debug - Semua Session State"):
        st.write(f"**Minat:** {st.session_state.get('minat', 'KOSONG')}")
        st.write(f"**Hard Skill:** {st.session_state.get('hard_skill', 'KOSONG')}")
        st.write(f"**Soft Skill:** {st.session_state.get('soft_skill', 'KOSONG')}")
        st.write(f"**Mapel:** {st.session_state.get('mapel', 'KOSONG')}")
        st.write(f"**Jurusan:** {st.session_state.get('jurusan_sekolah', 'KOSONG')}")
        st.write(f"**Personality:** {st.session_state.get('personality', 'KOSONG')}")
        st.write(f"**Hobi:** {st.session_state.get('hobi', 'KOSONG')}")
        st.write(f"**Ekskul:** {st.session_state.get('ekskul', 'KOSONG')}")
    
    required_fields = [
        'minat', 'hard_skill', 'soft_skill', 'mapel',
        'jurusan_sekolah', 'personality', 'hobi', 'ekskul'
    ]
    missing_fields = [field for field in required_fields if not st.session_state.get(field)]
    
    if missing_fields:
        st.warning("⚠️ Data tes belum lengkap. Lengkapi semua pilihan terlebih dahulu untuk melihat hasil rekomendasi.")
        st.write("Field yang belum terisi:", ', '.join(missing_fields))
        st.button("Kembali ke Tes", on_click=set_page, args=('q1',))
    elif model is None or tfidf is None:
        st.error("Model Machine Learning gagal dimuat.")
    else:
        with st.spinner("AI sedang menganalisis profilmu..."):
            # ==========================================
            # A. PREDIKSI FITUR UTAMA (Murni Machine Learning)
            # ==========================================
            minat = st.session_state.get('minat', '')
            hard_skill_list = st.session_state.get('hard_skill', [])
            soft_skill_list = st.session_state.get('soft_skill', [])
            mapel = st.session_state.get('mapel', '')
            prediksi_rf = None
            
            # Cek jika user belum mengisi apa-apa
            if minat == '' or len(hard_skill_list) == 0:
                st.warning("Sepertinya kamu belum menyelesaikan tes! Yuk, mulai dari awal.")
                st.button("Kembali ke Beranda", on_click=set_page, args=('home',))
                st.stop()
            else:
                # Gabungkan list menjadi string yang dipisahkan oleh spasi
                hard_skill_str = " ".join(hard_skill_list)
                soft_skill_str = " ".join(soft_skill_list)
                
                teks_gabungan = f"{minat} {hard_skill_str} {soft_skill_str} {mapel}"
                
                input_tfidf = tfidf.transform([teks_gabungan])
                prediksi_ml = model.predict(input_tfidf)
                prediksi_rf = str(le.inverse_transform(prediksi_ml)[0])
            
            
            # ==========================================
            # B. PERHITUNGAN SKOR PENDUKUNG
            # ==========================================
            skor = {
                "Komputer dan Teknologi": 0, "Teknik": 0, "Kesehatan": 0,
                "Ekonomi dan Bisnis": 0, "Pendidikan": 0, "Seni": 0,
                "Sosial dan Humaniora": 0, "Pertanian": 0, "Sains dan MIPA": 0
            }
            
            # 1. Skor Fitur Utama (Prediksi RF)
            if prediksi_rf in skor:
                skor[prediksi_rf] += 20
                
            # 2. Skor Jurusan (+15)
            for bidang in jurusan_dict.get(st.session_state.jurusan_sekolah, []):
                skor[bidang] += 15
                
            # 3. Skor Hobi (+10)
            for bidang in hobi_dict.get(st.session_state.hobi, []):
                skor[bidang] += 10
                
            # 4. Skor Ekskul (+5)
            for bidang in ekskul_dict.get(st.session_state.ekskul, []):
                skor[bidang] += 5
                
            # 5. Skor Personality (+10)
            for bidang in personality_dict.get(st.session_state.personality, []):
                skor[bidang] += 10
                
            # ==========================================
            # C. HASIL AKHIR (Top 3)
            # ==========================================
            ranking = sorted(skor.items(), key=lambda x: x[1], reverse=True)
            total_skor = sum(skor.values())
            if total_skor == 0: total_skor = 1 
            top_3 = ranking[:3]

        # Menampilkan UI Hasil
        st.markdown("---")
        st.write("Berdasarkan **Analisis Potensi Utama (AI) & Profil Keseharianmu**, ini adalah 3 bidang yang paling cocok untukmu:")
        
        st.success(f"🥇 **{top_3[0][0]}** — {round((top_3[0][1]/total_skor)*100, 2)}%")
        st.info(f"🥈 **{top_3[1][0]}** — {round((top_3[1][1]/total_skor)*100, 2)}%")
        st.warning(f"🥉 **{top_3[2][0]}** — {round((top_3[2][1]/total_skor)*100, 2)}%")
        
        st.markdown("---")
        st.subheader("Jurusan Populer untuk Setiap Rekomendasi")
        col1, col2, col3 = st.columns(3)
        desc1 = get_jurusan_populer_text(top_3[0][0])
        desc2 = get_jurusan_populer_text(top_3[1][0])
        desc3 = get_jurusan_populer_text(top_3[2][0])
        col1.markdown(f"**{top_3[0][0]}**")
        col1.markdown(desc1, unsafe_allow_html=True)
        col2.markdown(f"**{top_3[1][0]}**")
        col2.markdown(desc2, unsafe_allow_html=True)
        col3.markdown(f"**{top_3[2][0]}**")
        col3.markdown(desc3, unsafe_allow_html=True)
        
        st.write("### Apa langkah selanjutnya?")
        st.write(f"Bidang utama yang paling direkomendasikan adalah **{top_3[0][0]}**, namun kamu juga memiliki potensi kuat di **{top_3[1][0]}** dan **{top_3[2][0]}**. Cobalah mencari tahu lebih dalam tentang program studi atau profesi di ketiga bidang ini. Jangan ragu untuk mendiskusikannya dengan guru BK atau orang tuamu untuk memantapkan pilihan!")
        
        st.markdown("---")
        st.button("🔄 Ulangi Tes", on_click=reset_state)
