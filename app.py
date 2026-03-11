import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np

# --- СОСТОЯНИЕ (ТЕМА И ЯЗЫК) ---
if 'theme' not in st.session_state: st.session_state.theme = 'dark'
if 'lang' not in st.session_state: st.session_state.lang = 'RU'

# --- ТЕКСТЫ ---
texts = {
    'RU': {
        'name': 'ИШЕНБЕКОВ ЯСИР', 'loc': 'ЛОКАЦИЯ', 'school': 'ШКОЛА', 'city': 'Бишкек',
        'about_title': '👨‍💻 Обо мне', 
        'about_text': 'Я ученик школы ЭЭЛ №65 из города Бишкек. Интересуюсь IT, созданием сайтов и видеопроектами. Постоянно учусь и развиваюсь, собирая своё портфолио.',
        'contact': 'Связаться со мной', 'tab1': '🚀 МОИ ПРОЕКТЫ', 'tab2': '♻️ АНАЛИЗАТОР',
        'verdict': '🤖 Вердикт:', 'unknown': 'Не определено',
        'glass': 'Стекло', 'plastic': 'Пластик', 'paper': 'Бумага/Картон', 'metal': 'Металл'
    },
    'EN': {
        'name': 'YASIR ISHENBEKOV', 'loc': 'LOCATION', 'school': 'SCHOOL', 'city': 'Bishkek',
        'about_title': '👨‍💻 About Me', 
        'about_text': 'I am a student at school EEL No. 65 from Bishkek. I am interested in IT, web development and video projects. Constantly learning and growing my portfolio.',
        'contact': 'Contact me', 'tab1': '🚀 PROJECTS', 'tab2': '♻️ ANALYZER',
        'verdict': '🤖 Verdict:', 'unknown': 'Unknown',
        'glass': 'Glass', 'plastic': 'Plastic', 'paper': 'Paper/Cardboard', 'metal': 'Metal'
    }
}

L = texts[st.session_state.lang]

# --- КОНФИГ ---
st.set_page_config(page_title=L['name'], layout="wide")

# --- СТИЛИ ---
bg = "#080a0d" if st.session_state.theme == 'dark' else "#ffffff"
txt = "#e0e0e0" if st.session_state.theme == 'dark' else "#1a1a1a"
card = "rgba(255,255,255,0.03)" if st.session_state.theme == 'dark' else "#f8f9fa"
brd = "rgba(255,255,255,0.1)" if st.session_state.theme == 'dark' else "#e2e8f0"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg}; color: {txt}; }}
    .main-card {{ background: {card}; border: 1px solid {brd}; border-radius: 20px; padding: 30px; margin-bottom: 20px; }}
    .info-tag {{ background: {card}; border: 1px solid {brd}; padding: 8px 15px; border-radius: 10px; font-size: 0.9rem; }}
    .contact-btn {{ 
        display: inline-block; padding: 10px 20px; background: {card}; border: 1px solid {brd}; 
        border-radius: 10px; color: {txt} !important; text-decoration: none; transition: 0.3s; margin-right: 10px;
    }}
    .contact-btn:hover {{ border-color: #3b82f6; }}
    .video-box {{ background: {card}; border: 1px solid {brd}; border-radius: 15px; padding: 10px; }}
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    if st.button("🌓 Light / Dark"): 
        st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
        st.rerun()
    if st.button("🌐 RU / EN"): 
        st.session_state.lang = 'EN' if st.session_state.lang == 'RU' else 'RU'
        st.rerun()

# --- ШАПКА ---
st.markdown(f"""
<div class="main-card">
    <h1 style="margin:0; font-size: 2.8rem;">{L['name']}</h1>
    <div style="display: flex; gap: 15px; margin-top: 15px;">
        <div class="info-tag">📍 {L['city']}</div>
        <div class="info-tag">🏫 ЭЭЛ №65</div>
    </div>
    <div style="margin-top: 25px;">
        <h3>{L['about_title']}</h3>
        <p style="font-size: 1.1rem; opacity: 0.8; max-width: 800px;">{L['about_text']}</p>
    </div>
    <div style="margin-top: 20px;">
        <a href="https://wa.me/996507049" class="contact-btn">💬 WhatsApp</a>
        <a href="https://t.me/HewsTM" class="contact-btn">✈️ Telegram</a>
    </div>
</div>
""", unsafe_allow_html=True)

tabs = st.tabs([L['tab1'], L['tab2']])

with tabs[0]:
    v_col1, v_col2, v_col3 = st.columns(3)
    v_urls = ["https://youtu.be/cRumatSprfI", "https://youtu.be/IJQV8EpzCAI", "https://youtu.be/nG5uaU0ANJQ", "https://youtu.be/KpeUXmTIUuQ", "https://youtu.be/aN2W4JRKhTY"]
    for i, url in enumerate(v_urls):
        with [v_col1, v_col2, v_col3][i % 3]:
            st.markdown('<div class="video-box">', unsafe_allow_html=True); st.video(url); st.markdown('</div>', unsafe_allow_html=True)

with tabs[1]:
    up = st.file_uploader("Upload", type=["jpg","png","jpeg"], label_visibility="collapsed")
    if up:
        img = Image.open(up)
        with st.spinner('AI Thinking...'):
            model = tf.keras.applications.MobileNetV2(weights='imagenet')
            p_img = img.resize((224, 224))
            x = tf.keras.preprocessing.image.img_to_array(p_img)
            x = np.expand_dims(x, axis=0)
            x = tf.keras.applications.mobilenet_v2.preprocess_input(x)
            preds = model.predict(x)
            decoded = tf.keras.applications.mobilenet_v2.decode_predictions(preds, top=3)[0]

        # ПРОДВИНУТЫЙ МАППИНГ (ОБУЧЕНИЕ)
        mapping = {
            'bottle': L['glass'], 'wine': L['glass'], 'beaker': L['glass'], 'goblet': L['glass'],
            'water_bottle': L['plastic'], 'pill_bottle': L['plastic'], 'packet': L['plastic'], 'bag': L['plastic'],
            'carton': L['paper'], 'box': L['paper'], 'cardboard': L['paper'], 'envelope': L['paper'], 'menu': L['paper'],
            'can': L['metal'], 'tin': L['metal'], 'pot': L['metal'], 'brass': L['metal']
        }
        
        main_label = decoded[0][1].lower()
        verdict = L['unknown']
        for key, val in mapping.items():
            if key in main_label: verdict = val

        st.markdown(f'<div class="main-card" style="display:flex; gap:30px;">', unsafe_allow_html=True)
        c1, c2 = st.columns([1, 2])
        with c1: st.image(img, use_container_width=True)
        with c2:
            st.write(f"### {L['verdict']} {verdict}")
            for _, label, prob in decoded:
                st.write(f"**{label}**: {round(float(prob*100), 1)}%")
                st.progress(float(prob))
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f"<p style='text-align:center; opacity:0.3; margin-top:50px;'>© 2026 Ishenbekov Yasir</p>", unsafe_allow_html=True)
