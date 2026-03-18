import streamlit as st
import google.generativeai as genai

st.set_page_config(
    page_title="LinguistAI | Smart Contextual Translator",
    page_icon="🌐",
    layout="centered"
)

try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error("API Key tidak ditemukan. Pastikan Anda telah mengatur 'GEMINI_API_KEY' di Streamlit Secrets.")
    st.stop()

model = genai.GenerativeModel('gemini-2.5-flash')


st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stTextArea textarea { border-radius: 10px; border: 1px solid #ddd; }
    .stButton>button { 
        width: 100%; 
        border-radius: 8px; 
        height: 3em; 
        background-color: #007BFF; 
        color: white;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #0056b3; border: none; }
    .result-container { 
        padding: 20px; 
        background-color: #ffffff !important;
        color: #1a1a1a !important;          
        border-radius: 12px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 6px solid #007BFF;
    }
    .result-container p, .result-container span, .result-container li, .result-container strong {
        color: #1a1a1a !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🌐 LinguistAI")
st.markdown("### *Penerjemah Berbasis Konteks & AI*")
st.info("Aplikasi ini menggunakan LLM (Gemini AI) untuk memahami nuansa bahasa, bukan sekadar kata demi kata.")

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        source_lang = st.selectbox("Bahasa Asal:", ["Otomatis (Deteksi)", "Inggris", "Indonesia", "Jepang", "Korea", "Mandarin", "Arab", "Prancis", "Jerman"])
    with col2:
        target_lang = st.selectbox("Bahasa Tujuan:", ["Indonesia", "Inggris", "Jepang", "Korea", "Mandarin", "Arab", "Prancis", "Jerman"])

    tone = st.select_slider(
        "Pilih Gaya Bahasa (Tone):",
        options=["Sangat Santai (Slang)", "Santai", "Netral", "Formal", "Sangat Formal (Sopan)"]
    )

    text_input = st.text_area("Masukkan Kalimat:", placeholder="Ketik di sini...", height=150)

if st.button("Terjemahkan Sekarang"):
    if not text_input.strip():
        st.warning("Silakan masukkan teks terlebih dahulu!")
    else:
        with st.spinner("Sedang menganalisis konteks dan menerjemahkan..."):
            try:
                prompt = f"""
                Bertindaklah sebagai penerjemah ahli multibahasa. 
                Tugasmu adalah menerjemahkan teks berikut:
                
                Teks: "{text_input}"
                Dari: {source_lang}
                Ke: {target_lang}
                Gaya Bahasa: {tone}
                
                Berikan respon dalam format berikut:
                1. **Terjemahan Utama**: Hasil terjemahan yang paling natural.
                2. **Analisis Konteks**: Jelaskan singkat mengapa kata-kata tersebut dipilih berdasarkan gaya bahasa '{tone}'.
                3. **Saran Alternatif**: Berikan 1 variasi cara bicara lain untuk kalimat yang sama.
                """

                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.subheader("Hasil Terjemahan LinguistAI:")
                st.markdown(f"""
                <div class="result-container">
                    {response.text}
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Terjadi kesalahan teknis: {str(e)}")
    
st.markdown("---")
st.markdown(
    "<center><p style='color: gray;'>LinguistAI v1.0 | Project Informatika</p></center>", 
    unsafe_allow_html=True
)