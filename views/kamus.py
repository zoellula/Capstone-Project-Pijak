import streamlit as st

# === FUNGSI UI ====
def create_checkbox_group_max3(items_dict, session_key, label_text, max_selections=3):
    st.write(f"**{label_text}** (maksimal {max_selections} pilihan)")

    options = list(items_dict.keys())
    cols = st.columns(2)

    selected = st.session_state.get(session_key, [])
    if not isinstance(selected, list):
        selected = []

    checked_count = sum(1 for _ in selected)

    for i, option in enumerate(options):
        widget_key = f"{session_key}_{option}"
        is_checked = option in selected
        disabled = (checked_count >= max_selections) and (not is_checked)

        with cols[i % 2]:
            if st.checkbox(
                option.title(),
                value=is_checked,
                key=widget_key,
                disabled=disabled,
            ):
                if option not in selected:
                    selected.append(option)
            else:
                if option in selected:
                    selected.remove(option)

    st.session_state[session_key] = selected
    return selected

def create_radio_by_category(items_dict, session_key, label_text):
    st.write(f"**{label_text}**")

    options = list(items_dict.keys())
    cols = st.columns(2)

    current_value = st.session_state.get(session_key, "")

    for i, option in enumerate(options):
        with cols[i % 2]:

            checked = st.checkbox(
                option.title(),
                value=(current_value == option),
                key=f"{session_key}_{option}")

            if checked and current_value != option:
                st.session_state[session_key] = option
                st.rerun()

def create_minat_accordion(items_dict, session_key, label_text):
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

                with cols[i % 2]:

                    widget_key = f"{session_key}_{opt}"
                    is_selected = (current_value == opt)

                    checked = st.checkbox(
                        opt.title(),
                        value=is_selected,
                        key=widget_key,
                        disabled=is_selected,
                    )

                    # Jika user klik opsi non-aktif, lakukan switch ke opsi baru.
                    if checked and current_value != opt:
                        st.session_state[session_key] = opt
                        st.rerun()

    return st.session_state.get(session_key, "")


def create_checkbox_group(items_dict, session_key, label_text):
    """Multi-select maksimal 2 pilihan, disimpan ke st.session_state[session_key] sebagai list pilihan."""
    st.write(f"**{label_text}** (Maksimal 2 pilihan)")

    options = list(items_dict.keys())
    selected = st.session_state.get(session_key, [])
    if not isinstance(selected, list):
        selected = []

    checked_count = len(selected)
    cols = st.columns(2)

    for i, option in enumerate(options):
        widget_key = f"{session_key}_{option}"
        is_checked = option in selected
        disabled = (checked_count >= 2) and (not is_checked)

        with cols[i % 2]:
            if st.checkbox(
                option.title(),
                value=is_checked,
                key=widget_key,
                disabled=disabled,
            ):
                if option not in selected:
                    selected.append(option)
            else:
                if option in selected:
                    selected.remove(option)

    st.session_state[session_key] = selected
    return selected



def get_selected_checkboxes(items_dict, session_key):
    selected = []
    for option in items_dict.keys():
        widget_key = f"{session_key}_{option}"
        if st.session_state.get(widget_key, option in st.session_state.get(session_key, [])):
            selected.append(option)
    return selected

def create_support_accordion(items_dict, session_key, label_text):
    st.write(f"**{label_text}**")

    # kelompokkan option berdasarkan bidang
    categories = []
    cat_items = {}

    for option, bidang_list in items_dict.items():

        if not isinstance(bidang_list, list):
            bidang_list = [bidang_list]

        for bidang in bidang_list:

            if bidang not in cat_items:
                cat_items[bidang] = []
                categories.append(bidang)

            cat_items[bidang].append(option)

    selected = st.session_state.get(session_key, [])

    if not isinstance(selected, list):
        selected = []

    # tampilkan seperti Step 1
    for bidang in categories:

        expanded = any(opt in selected for opt in cat_items[bidang])

        with st.expander(bidang.upper(), expanded=expanded):

            cols = st.columns(2)

            for i, option in enumerate(cat_items[bidang]):

                with cols[i % 2]:

                    checked = option in selected

                    checkbox_key = f"{session_key}_{bidang}_{option}"
                    if st.checkbox(
                        option.title(),
                        value=checked,
                        key=checkbox_key
                    ):
                        if option not in selected:
                            selected.append(option)

                    else:
                        if option in selected:
                            selected.remove(option)

    st.session_state[session_key] = selected
    return selected


def get_jurusan_populer_text(bidang):
    if bidang == "Komputer dan Teknologi": return "Teknik Informatika<br>Sistem Informasi<br>Ilmu Komputer<br>Teknologi Informasi<br>Sistem Komputer"

    elif bidang == "Teknik": return "Teknik Industri<br>Teknik Sipil<br>Teknik Mesin<br>Teknik Elektro<br>Teknik Kimia"
    elif bidang == "Kesehatan": return "Kedokteran<br>Keperawatan<br>Farmasi<br>Kesehatan Masyarakat<br>Gizi"
    elif bidang == "Ekonomi dan Bisnis": return "Akuntansi<br>Manajemen<br>Bisnis Digital<br>Kewirausahaan<br>Ekonomi Pembangunan<br>"
    elif bidang == "Pendidikan": return "PGSD<br>PGPAUD<br>Pendidikan Bahasa Inggris<br>Pendidikan Matematika<br>Pendidikan Bahasa Indonesia"
    elif bidang == "Seni": return "DKV<br>Seni Rupa<br>Desain Produk<br>Film<br>Fotografi"
    elif bidang == "Sosial dan Humaniora": return "Hukum<br>Psikologi<br>Ilmu Komunikasi<br>Hubungan Internasional<br>Administrasi Publik"
    elif bidang == "Pertanian": return "Agribisnis<br>Agroteknologi<br>Teknologi Pangan<br>Peternakan<br>Kehutanan"
    elif bidang == "Sains dan MIPA": return "Matematika<br>Statistika<br>Fisika<br>Kimia<br>Biologi"
    else: return "Agribisnis<br>Agroteknologi<br>Teknologi Pangan<br>Peternakan<br>Kehutanan"

# === KAMUS DATA (DICTIONARY) === #
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