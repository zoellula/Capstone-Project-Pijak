import streamlit as st

# === FUNGSI UI ====
def create_radio_group(items_dict, session_key):
    """Tampilkan pilihan sebagai radio button untuk satu pilihan saja."""
    options = list(items_dict.keys())
    current_value = st.session_state.get(session_key, "")

    if isinstance(current_value, list):
        current_value = current_value[0] if current_value else ""

    index = options.index(current_value) if current_value in options else 0

    selected = st.radio(
        "",
        options,
        index=index,
        format_func=lambda x: x.title(),
        key=f"{session_key}_radio_group",
        horizontal=False,
        label_visibility="collapsed",
    )

    st.session_state[session_key] = selected
    return selected

def create_minat_accordion(items_dict, session_key, label_text, terjemahan_minat):
    st.write(f"**{label_text}**")

    categories = []
    cat_items = {}

    for opt, cat in items_dict.items():
        if cat not in cat_items:
            cat_items[cat] = []
            categories.append(cat)

        cat_items[cat].append(opt)

    current_value = st.session_state.get(session_key, "")
    if isinstance(current_value, list):
        current_value = current_value[0] if current_value else ""

    for cat in categories:

        expanded = current_value in cat_items[cat]

        with st.expander(cat.upper(), expanded=expanded):

            cols = st.columns(2)

            for i, opt in enumerate(cat_items[cat]):

                with cols[i % 2]:

                    widget_key = f"{session_key}_{opt}"
                    is_selected = (current_value == opt)

                    # === PENERAPAN TOPENG BAHASA ===
                    if terjemahan_minat:
                        label_tampil = terjemahan_minat.get(opt, opt.title())
                    else:
                        label_tampil = opt.title()

                    checked = st.checkbox(
                        label_tampil,
                        value=is_selected,
                        key=widget_key,
                        #disabled=is_selected,
                    )

                    # Jika user klik opsi non-aktif, lakukan switch ke opsi baru.
                    #if checked and current_value != opt:
                    #    st.session_state[session_key] = opt
                    #    st.rerun()

    return st.session_state.get(session_key, "")


def create_checkbox_group(items_dict, session_key, label_text, translation_dict=None):
    """Multi-select maksimal 2 pilihan, disimpan ke st.session_state[session_key] sebagai list pilihan."""
    st.write(f"**{label_text}**")

    options = list(items_dict.keys())
    selected = st.session_state.get(session_key, [])
    if not isinstance(selected, list):
        selected = []

    checked_count = len(selected)
    cols = st.columns(2)

    for i, option in enumerate(options):
        widget_key = f"{session_key}_{option}"
        is_checked = option in selected
        #disabled = (checked_count >= 2) and (not is_checked)
        
        # === PENERAPAN TOPENG BAHASA ===
        if translation_dict:
            label_tampil = translation_dict.get(option, option.title())
        else:
            label_tampil = option.title()

        with cols[i % 2]:
            if st.checkbox(
                label_tampil,
                value=is_checked,
                key=widget_key,
                #disabled=disabled,
            ):
                if option not in selected:
                    selected.append(option)
            else:
                if option in selected:
                    selected.remove(option)

    st.session_state[session_key] = selected
    return selected


def create_single_checkbox_group(items_dict, session_key, detail_jurusan=None):
    """Menampilkan pilihan checkbox dan menyimpan semua yang dicentang dalam bentuk List."""
    options = list(items_dict.keys())
    
    # Pastikan data yang diambil bentuknya adalah List []
    selected_list = st.session_state.get(session_key, [])
    if not isinstance(selected_list, list):
        selected_list = []

    # Siapkan keranjang kosong untuk menampung centangan user saat ini
    current_selections = []
    
    cols = st.columns(2)

    for i, option in enumerate(options):
        with cols[i % 2]:
            # Cek apakah opsi ini sebelumnya ada di keranjang
            is_checked = option in selected_list
            
            # Tentukan label tampilan: jika ada di detail_jurusan, pakai itu.
            # Jika tidak ada, pakai default (option.title())
            label_tampil = detail_jurusan.get(option, option.title()) if detail_jurusan else option.title()

            # Render checkbox (key dibedakan sedikit agar tidak bentrok dengan session_key utama)
            checked = st.checkbox(
                label_tampil,
                value=is_checked,
                key=f"widget_{session_key}_{option}"
            )

            # Jika user mencentang ini, masukkan ke keranjang
            if checked:
                current_selections.append(option)

    # Simpan keranjang yang sudah berisi pilihan user ke memori utama
    st.session_state[session_key] = current_selections
    
    return current_selections


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
    if bidang == "Komputer dan Teknologi": return "Bidang ini mencakup ilmu pengetahuan yang sangat luas. Pada bidang ini kamu akan belajar tentang seluk beluk perangkat keras maupun lunak. Termasuk bagaimana cara membuat dan mengoperasikannya dengan baik.<p>Beberapa jurusan rekomendasi yang bisa dipilih yaitu:<br>Teknik Informatika<br>Sistem Informasi<br>Ilmu Komputer<br>Teknologi Informasi<br>Sistem Komputer"
    elif bidang == "Teknik": return "Pada bidang ini kamu akan belajar menciptakan, mendesain, memperbaiki, dan melakukan riset mesin gedung, program komputer, dan lain sebagainya. Bidang ini sampai sekarang masih berkembang dan menyesuaikan dengan kebutuhan masyarakat modern.<p>Beberapa jurusan rekomendasi yang bisa dipilih yaitu:<br>Teknik Industri<br>Teknik Sipil<br>Teknik Mesin<br>Teknik Elektro<br>Teknik Kimia"
    elif bidang == "Kesehatan": return "Di bidang ini kamu akan mempelajari tentang kesehatan individu maupun masyarakat. Termasuk hal yang menunjang kesehatan seperti kondisi lingkungan, obat-obatan, teknologi kesehatan, dan lain sebagainya.<p>Beberapa jurusan rekomendasi yang bisa dipilih yaitu:<br>Kedokteran<br>Keperawatan<br>Farmasi<br>Kesehatan Masyarakat<br>Gizi"
    elif bidang == "Ekonomi dan Bisnis": return "Sekarang, bidan ini menjadi salah satu bidang yang banyak digemari oleh anak muda. Bidang ini mencakup berbagai disiplin ilmu sosial lain seperti produksi, distribusi, perdagangan, pariwisata, dan lain sebagainya.<p>Beberapa jurusan rekomendasi yang bisa dipilih yaitu:<br>Akuntansi<br>Manajemen<br>Bisnis Digital<br>Kewirausahaan<br>Ekonomi Pembangunan<br>"
    elif bidang == "Pendidikan": return "Bidang ini akan mempelajari tentang berbagai macam hal yang mendukung pendidikan. Salah satunya tentang teknologi yang mendukung pendidikan.<p>Beberapa jurusan rekomendasi yang bisa dipilih yaitu:<br>PGSD<br>PGPAUD<br>Pendidikan Bahasa Inggris<br>Pendidikan Matematika<br>Pendidikan Bahasa Indonesia"
    elif bidang == "Seni": return "Bidang ini bisa dipilih untuk kamu yang kreatif. Seni zaman sekarang sudah cukup maju dan menyesuaikan dengan teknologi. Kamu juga akan belajar banyak hal tentang ilmu-ilmu yang berhubungan dengan desain.<p>Beberapa jurusan rekomendasi yang bisa dipilih yaitu:<br>DKV<br>Seni Rupa<br>Desain Produk<br>Film<br>Fotografi"
    elif bidang == "Sosial dan Humaniora": return "Bidang ini sangat erat kaitannya dengan ilmu-ilmu yang berhubungan dengan manusia, atau ilmu sosial. Bidang ini mempunyai cakupan yang luas sehingga menjadi pilihan banyak mahasiswa yang menyukai ilmu-ilmu sosial.<p>Beberapa jurusan rekomendasi yang bisa dipilih yaitu:<br>Hukum<br>Psikologi<br>Ilmu Komunikasi<br>Hubungan Internasional<br>Administrasi Publik"
    elif bidang == "Pertanian": return "Bidang ini akan belajar banyak hal tentang ilmu bertani. Termasuk pengelolaan tanaman di kebun, sawah, dan ladang. Tidak hanya itu, kamu juga akan belajar tentang mikrobiologi pertanian dan ilmu-ilmu lain yang relevan dengan ilmu bertani.<p>Beberapa jurusan rekomendasi yang bisa dipilih yaitu:<br>Agribisnis<br>Agroteknologi<br>Teknologi Pangan<br>Peternakan<br>Kehutanan"
    elif bidang == "Sains dan MIPA": return "Bidang ini adalah bidang studi yang menaungi jurusan ilmu-ilmu eksak. Ilmu pengetahuan yang berada di bawah bidang ini berkembang sesuai dengan perkembangan zaman. Bahkan, bidang ini sudah mencakup astronomi dan bioteknologi.<p>Beberapa jurusan rekomendasi yang bisa dipilih yaitu:<br>Matematika<br>Statistika<br>Fisika<br>Kimia<br>Biologi"

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

# Kamus terjemahan hanya untuk tampilan UI (User Interface)
terjemahan_minat = {
    # Komputer & Teknologi
    "coding": "Pemrograman (Coding)", 
    "programming": "Pemrograman", 
    "artificial intelligence": "Kecerdasan Buatan (AI)", 
    "machine learning": "Pembelajaran Mesin (Machine Learning)", 
    "web development": "Pengembangan Web", 
    "software": "Perangkat Lunak", 
    "cyber security": "Keamanan Siber", 
    "data science": "Ilmu Data", 
    "game development": "Pengembangan Game", 
    "technology": "Teknologi", 
    "information technology": "Teknologi Informasi (TI)", 
    "it": "IT (Teknologi Informasi)", 
    "cloud computing": "Komputasi Awan (Cloud Computing)", 
    "data analytics": "Analisis Data", 
    "data scientist": "Ilmuwan Data (Data Scientist)", 
    "web designing": "Desain Web", 
    "blockchain": "Teknologi Blockchain", 
    "software developer": "Pengembang Perangkat Lunak", 
    "software engineer": "Rekayasa Perangkat Lunak",
    
    # Teknik
    "robotics": "Robotika", 
    "mechanics": "Mekanika / Mesin", 
    "electronics": "Elektronika", 
    "automobile": "Otomotif", 
    "construction": "Konstruksi", 
    "engineering": "Teknik Umum", 
    "oil and gas": "Minyak dan Gas", 
    "project management": "Manajemen Proyek", 
    "construction manegement": "Manajemen Konstruksi", 
    "infrastructure": "Infrastruktur",
    
    # Kesehatan
    "doctor": "Kedokteran", 
    "medical": "Medis", 
    "pharmacy": "Farmasi", 
    "nutrition": "Gizi/Nutrisi", 
    "healthcare": "Kesehatan Masyarakat", 
    "understand human body": "Anatomi Tubuh Manusia", 
    "medicine": "Ilmu Pengobatan",
    
    # Bisnis
    "business": "Bisnis", 
    "finance": "Keuangan", 
    "marketing": "Pemasaran (Marketing)", 
    "entrepreneurship": "Kewirausahaan", 
    "accounting": "Akuntansi", 
    "financial analysis": "Analisis Keuangan", 
    "sales/marketing": "Penjualan / Pemasaran", 
    "trading": "Perdagangan (Trading)", 
    "market reserach": "Riset Pasar", 
    "business analytics": "Analisis Bisnis", 
    "supply chain analysis": "Analisis Rantai Pasok",
    
    # Pendidikan
    "teaching": "Mengajar", 
    "education": "Pendidikan", 
    "govt. job": "Instansi Pemerintah",
    "government jobs": "Aparatur Sipil Negara (ASN)",

    #Seni
    "music": "Musik",
    "drawing": "Menggambar",
    "photography": "Fotografi",
    "animation": "Animasi",
    "design": "Desain",
    "video editing": "Pengeditan Video",
    "home interior design": "Desain Interior Rumah",

    #Sosial dan Humaniora
    "psychology": "Psikologi",
    "law": "Hukum",
    "journalism": "Jurnalistik",
    "communication": "Komunikasi",
    "politics": "Politik",

    #Pertanian
    "farming": "Bertani",
    "agriculture": "Pertanian",
    "livestock": "Peternakan",
    "plant cultivation": "Budidaya Tanaman",
    "gardening": "Berkebun",

    #Sains dan MIPA
    "mathematics": "Matematika",
    "physics": "Fisika",
    "chemistry": "Kimia",
    "biology": "Biologi",
    "research": "Riset",
    "science": "Ilmu Pengetahuan Alam"
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

# Kamus terjemahan hanya untuk tampilan UI (User Interface)
terjemahan_hard = {
    # Komputer & Teknologi
    "programming": "Pemrograman",
    "coding": "Penulisan Kode (Coding)",
    "python": "Bahasa Python",
    "java": "Bahasa Java",
    "c++": "Bahasa C++",
    "web development": "Pengembangan Web",
    "software development": "Pengembangan Perangkat Lunak",
    "machine learning": "Pembelajaran Mesin (Machine Learning)",
    "artificial intelligence": "Kecerdasan Buatan (AI)",
    "database": "Basis Data",
    "data analysis": "Analisis Data",
    "networking": "Jaringan Komputer",
    "cyber security": "Keamanan Siber",

    # Teknik
    "autocad": "Aplikasi AutoCAD",
    "machining": "Pemesinan",
    "mechanical repair": "Perbaikan Mekanik",
    "electrical wiring": "Kelistrikan",
    "electronics": "Elektronik",
    "robotics": "Robotika",
    "circuit design": "Desain Sirkuit",
    "engineering drawing": "Gambar Teknik",
    "civil": "Teknik Sipil",

    # Kesehatan
    "patient care": "Perawatan Pasien",
    "medical knowledge": "Pengetahuan Medis",
    "clinical analysis": "Analisis Klinis",
    "pharmaceutical knowledge": "Pengetahuan Farmasi",
    "nutrition analysis": "Analisis Gizi",
    
    # Ekonomi dan Bisnis
    "accounting": "Akuntansi",
    "finance": "Keuangan",
    "marketing": "Pemasaran (Marketing)",
    "sales": "Penjualan",
    "business analysis": "Analisis Bisnis",
    "bookkeeping": "Pembukuan",
    "management": "Manajemen",
    
    # Pendidikan
    "teaching": "Mengajar",
    "lesson planning": "Penyusunan Perencanaan Pembelajaran",
    "mentoring": "Pembimbingan (Mentoring)",
    "curriculum design": "Perancangan Kurikulum",
    
    # Seni
    "graphic design": "Desain Grafis",
    "animation": "Animasi",
    "video editing": "Pengeditan Video",
    "drawing": "Menggambar",
    "photography": "Fotografi",
    "music production": "Produksi Musik",
    "fashion design": "Desain Fashion",

    # Sosial dan Humaniora 
    "public speaking": "Berbicara di Depan Umum (Public Speaking)",
    "journalism": "Jurnalistik",
    "writing": "Menulis",
    "legal analysis": "Analisis Hukum",
    "communication": "Komunikasi",
    "foreign language": "Bahasa Asing",
    "negotiation": "Negosiasi",
    
    # Pertanian
    "farming": "Bertani",
    "plant cultivation": "Budidaya Tanaman",
    "soil analysis": "Analisis Tanah",
    "agricultural technology": "Teknologi Pertanian",
    "livestock management": "Manajemen Peternakan",

    # Sains dan MIPA
    "mathematics": "Matematika",
    "statistics": "Statistika",
    "research": "Riset",
    "laboratory analysis": "Analisis Laboratorium",
    "scientific analysis": "Analisis Ilmiah",
    "physics calculation": "Perhitungan Fisika",
    "chemical analysis": "Analisis Kimia"
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
# Kamus terjemahan hanya untuk tampilan UI (User Interface)
terjemahan_mapel = {
    # Komputer & Teknologi
    "computer science engineering": "Teknik Informatika",
    "computer science": "Ilmu Komputer",
    "computer applications": "Aplikasi Komputer",
    "information technology": "Teknologi Informasi",
    "programming": "Pemrograman",
    "coding": "Penulisan Kode",
    "software development": "Pengembangan Perangkat Lunak",
    "structural engineeeing": "Teknik Struktural",

    # Teknik
    "mechanical engineering": "Teknik Mesin",
    "civil engineering": "Teknik Sipil",
    "electrical engineering": "Teknik Elektro",
    "electrical and electronics engineering": "Teknik Elektro dan Elektronika",
    "electronics and communication engineering": "Teknik Elektronika dan Komunikasi",
    "automobile engineering": "Teknik Otomotif",
    "chemical engineering": "Teknik Kimia",
    "instrumentation engineering": "Teknik Instrumentasi",
    "structural engineering": "Teknik Struktural",
    "engineering": "Teknik/Rekayasa",
    "aeronautical": "Teknik Penerbangan",
    "autocad": "AutoCAD",

    # Kesehatan
    "pharmacy": "Farmasi",
    "dental surgeon": "Dokter Gigi",
    "dietician": "Ilmu Gizi",
    "hospital administration": "Administrasi Rumah Sakit",

    # Ekonomi dan Bisnis
   "commerce": "Perdagangan",
   "accountancy": "Akuntansi",
   "finance": "Keuangan",
   "business administration": "Administrasi Bisnis",
   "marketing": "Pemasaran",
   "sales & marketing": "Penjualan dan Pemasaran",
   "accounting": "Akuntansi",
   "economics": "Ekonomi",
   "business": "Bisnis",

    # Pendidikan
    "education": "Pendidikan",
    "general studies": "Pengetahuan Umum",
    "Bahasa Indonesia": "Bahasa Indonesia",

    # Seni
    "Seni Budaya": "Seni Budaya",
    "Desain Grafis": "Desain Grafis",
    "Multimedia": "Multimedia",
    "animation": "Animasi",
    "animation & visual effects": "Animasi dan Efek Visual",
    "fashion designing": "Desain Fashion",
    "interior design": "Desain Interior",
    "design": "Desain",
    "advertising": "Periklanan",

    #Sosial dan Humaniora
    "psychology": "Psikologi",
    "history": "Sejarah",
    "political science": "Ilmu Politik",
    "law": "Hukum",
    "journalism": "Jurnalistik",
    "english": "Bahasa Inggris",
    "sociology": "Sosiologi",
    "literature": "Sastra",

    # Pertanian
    "agriculture": "Pertanian",
    "agriculture engineering": "Teknik Pertanian",
    "agriculture biotechnalogy": "Bioteknologi Pertanian",
    
    # Sains dan MIPA
    "mathematics": "Matematika",
    "physics": "Fisika",
    "chemistry": "Kimia",
    "statistics": "Statistika",
    "science": "Ilmu Pengetahuan Alam",
    "biotechnology": "Bioteknologi",
    "bio technology": "Bioteknologi",   
    "botany": "Botani",
    "microbiology": "Mikrobiologi"
}

jurusan_dict = {
    "IPA": [ "Sains dan MIPA", "Kesehatan", "Teknik"],
    "IPS": ["Ekonomi dan Bisnis", "Sosial dan Humaniora"],
    "Bahasa": ["Pendidikan", "Sosial dan Humaniora", "Seni"],
    "Rekayasa Perangkat Lunak": ["Komputer dan Teknologi"],
    "TKJ": ["Komputer dan Teknologi"],
    # Sistem Informatika Jaringan dan Aplikasi
    "SIJA": ["Komputer dan Teknologi"],
    # Pengembangan Perangkat Lunak dan Gim
    "PPLG": ["Komputer dan Teknologi"],
    "Akuntansi": ["Ekonomi dan Bisnis"],
    # Akuntansi dan Keuangan Lembaga
    "AKL": [ "Ekonomi dan Bisnis"],
    "Perbankan": ["Ekonomi dan Bisnis"],
    "Manajemen Perkantoran": ["Ekonomi dan Bisnis"],
    # Otomatisasi dan Tata Kelola Perkantoran
    "OTKP": ["Ekonomi dan Bisnis"],
    "Bisnis Daring dan Pemasaran ": ["Ekonomi dan Bisnis"],
    "Pemasaran": ["Ekonomi dan Bisnis"],
    "Administrasi Perkantoran": ["Ekonomi dan Bisnis"],
    "Kuliner": ["Ekonomi dan Bisnis"],
    "Tata Boga": ["Ekonomi dan Bisnis"],
    "Teknik Kendaraan Ringan": ["Teknik"],
    #Teknik dan Bisnis Sepeda Motor
    "TBSM": ["Teknik"],
    "Teknik Mesin": ["Teknik"],
    "Teknik Elektro": ["Teknik"],
    "Teknik Otomotif": ["Teknik"],
    "Teknik Pengelasan": ["Teknik"],
    #Teknik Mesin
    "Teknik Pemesinan": ["Teknik"],
    "Teknik Industri": ["Teknik"],
    "Teknik Pendingin dan Tata Udara": ["Teknik"],
    "Teknik Konstruksi": ["Teknik"],
    "Teknik Sipil": ["Teknik"],
    "Teknik Energi Terbarukan": ["Teknik"],
    "Mekatronika": ["Teknik"],
    "Teknik Alat Berat": ["Teknik"],
    "Farmasi": ["Kesehatan"],
    "Keperawatan": ["Kesehatan"],
    "Analis Kesehatan": ["Kesehatan"],
    "Seni Musik": ["Seni"],
    "Seni Tari": ["Seni"],
    "Seni Rupa": ["Seni"],
    "Agribisnis Tanaman": ["Pertanian"],
    "Agribisnis Perikanan": ["Pertanian"],
    "Agribisnis Ternak": ["Pertanian"],
    "Kehutanan": ["Pertanian"],
    "Perhotelan": ["Ekonomi dan Bisnis", "Sosial dan Humaniora"],
    "Broadcasting": ["Seni", "Sosial dan Humaniora"],
    "Multimedia": ["Komputer dan Teknologi",  "Seni"],
    "Animasi": ["Komputer dan Teknologi", "Seni"],
    "Perhotelan": [ "Ekonomi dan Bisnis", "Sosial dan Humaniora"],
    "Desain Komunikasi Visual": ["Komputer dan Teknologi", "Seni"],
    "Usaha Perjalanan Wisata": ["Sosial dan Humaniora", "Ekonomi dan Bisnis"],
    "Tata Busana": ["Seni",  "Ekonomi dan Bisnis"]

}

detail_jurusan ={
    "TKJ": "Teknik Komputer dan Jaringan",
    "SIJA": "Sistem Informatika Jaringan dan Aplikasi",
    "PPLG": "Pengembangan Perangkat Lunak dan Gim",
    "AKL": "Akuntansi dan Keuangan Lembaga",
    "OTKP": "Otomatisasi dan Tata Kelola Perkantoran",
    "TBSM": "Teknik dan Bisnis Sepeda Motor",
    "Teknik Pemesinan": "Teknik Mesin"
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