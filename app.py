import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np

# --- ИНИЦИАЛИЗАЦИЯ ---
if 'theme' not in st.session_state: st.session_state.theme = 'dark'
if 'lang' not in st.session_state: st.session_state.lang = 'RU'

# --- СЛОВАРЬ И ОБУЧЕНИЕ ---
texts = {
    'RU': {
        'name': 'ИШЕНБЕКОВ ЯСИР', 'city': 'Бишкек', 'school': 'ЭЭЛ №65',
        'about': 'Я ученик 8-го класса из Бишкека. Разрабатываю IT-проекты, увлекаюсь искусственным интеллектом и экологией. Это моё цифровое пространство.',
        'projects': '🚀 ПРОЕКТЫ', 'analyzer': '♻️ WASTE AI',
        'verdict': 'ВЕРДИКТ:', 'unknown': 'Анализируем...',
        'glass': 'Стекло', 'plastic': 'Пластик', 'paper': 'Бумага / Картон', 'metal': 'Металл',
        'contact': 'СВЯЗЬ', 'soon': 'Скоро будет...', 'upload': 'Загрузите фото для сканирования'
    },
    'EN': {
        'name': 'YASIR ISHENBEKOV', 'city': 'Bishkek', 'school': 'EEL No. 65',
        'about': '8th-grade student from Bishkek. Developing IT projects, passionate about AI and ecology. This is my digital space.',
        'projects': '🚀 PROJECTS', 'analyzer': '♻️ WASTE AI',
        'verdict': 'VERDICT:', 'unknown': 'Analyzing...',
        'glass': 'Glass', 'plastic': 'Plastic', 'paper': 'Paper / Cardboard', 'metal': 'Metal',
        'contact': 'CONTACT', 'soon': 'Coming soon...', 'upload': 'Upload a photo to scan'
    }
}

L = texts[st.session_state.lang]

# --- КОНФИГУРАЦИЯ ---
st.set_page_config(page_title=L['name'], layout="wide")

# Цвета
if st.session_state.theme == 'dark':
    bg, txt, card, brd = "#05070a", "#ffffff", "rgba(255,255,255,0.03)", "rgba(255,255,255,0.08)"
    accent = "#3b82f6"
else:
    bg, txt, card, brd = "#f8f9fa", "#111827", "#ffffff", "#e5e7eb"
    accent = "#2563eb"

# --- СТИЛИ ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg}; color: {txt}; }}
    .main-card {{
        background: {card}; border: 1px solid {brd}; border-radius: 24px; padding: 40px; margin-bottom: 30px;
        backdrop-filter: blur(10px);
    }}
    .video-card {{
        border: 1px solid {brd}; border-radius: 16px; overflow: hidden; background: #000; margin-bottom: 20px;
        transition: 0.3s ease;
    }}
    .video-card:hover {{ border-color: {accent}; transform: translateY(-5px); }}
    .soon-card {{
        border: 1px dashed {brd}; border-radius: 16px; height: 210px;
        display: flex; align-items: center; justify-content: center; opacity: 0.4;
    }}
    .contact-btn {{
        display: inline-block; padding: 12px 28px; border-radius: 12px; font-weight: 600;
        text-decoration: none; margin-right: 12px; transition: 0.3s;
    }}
    .wa {{ background: #25d366; color: white !important; }}
    .tg {{ background: #0088cc; color: white !important; }}
    .ai-box {{ background: {card}; border: 1px solid {brd}; border-radius: 20px; padding: 30px; }}
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### DESIGN")
    if st.button("🌓 Switch Theme", use_container_width=True):
        st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
        st.rerun()
    if st.button("🌐 RU / EN", use_container_width=True):
        st.session_state.lang = 'EN' if st.session_state.lang == 'RU' else 'RU'
        st.rerun()

# --- HEADER ---
st.markdown(f"""
<div class="main-card">
    <h1 style="margin:0; font-size: 3.5rem; font-weight: 800; letter-spacing: -2px;">{L['name']}</h1>
    <p style="opacity: 0.5; font-size: 1.1rem; margin-bottom: 25px;">📍 {L['city']} &nbsp;•&nbsp; 🏫 {L['school']}</p>
    <p style="font-size: 1.25rem; line-height: 1.6; max-width: 850px; opacity: 0.9;">{L['about']}</p>
    <div style="margin-top: 35px;">
        <a href="https://wa.me/996507049" class="contact-btn wa">WhatsApp</a>
        <a href="https://t.me/HewsTM" class="contact-btn tg">Telegram</a>
    </div>
</div>
""", unsafe_allow_html=True)

tabs = st.tabs([L['projects'], L['analyzer']])

with tabs[0]:
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3, gap="large")
    urls = [
        "https://youtu.be/cRumatSprfI", "https://youtu.be/IJQV8EpzCAI",
        "https://youtu.be/nG5uaU0ANJQ", "https://youtu.be/KpeUXmTIUuQ",
        "https://youtu.be/aN2W4JRKhTY"
    ]
    for i, url in enumerate(urls):
        with [c1, c2, c3][i % 3]:
            st.markdown('<div class="video-card">', unsafe_allow_html=True); st.video(url); st.markdown('</div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="soon-card">{L["soon"]}</div>', unsafe_allow_html=True)

with tabs[1]:
    st.markdown("<br>", unsafe_allow_html=True)
    up = st.file_uploader(L['upload'], type=["jpg","png","jpeg"], label_visibility="collapsed")
    if up:
        img = Image.open(up)
        with st.spinner('Neural Processing...'):
            model = tf.keras.applications.MobileNetV2(weights='imagenet')
            p_img = img.resize((224, 224))
            x = np.expand_dims(tf.keras.preprocessing.image.img_to_array(p_img), axis=0)
            x = tf.keras.applications.mobilenet_v2.preprocess_input(x)
            preds = model.predict(x)
            decoded = tf.keras.applications.mobilenet_v2.decode_predictions(preds, top=3)[0]

        # --- ADVANCED AI TRAINING (MAPPING) ---
        mapping = {
            'bottle': L['glass'], 'wine': L['glass'], 'beaker': L['glass'], 'jug': L['glass'], 'vial': L['glass'],
            'plastic': L['plastic'], 'bag': L['plastic'], 'wrapper': L['plastic'], 'tub': L['plastic'], 'soap': L['plastic'],
            'paper': L['paper'], 'box': L['paper'], 'cardboard': L['paper'], 'envelope': L['paper'], 'packet': L['paper'], 'menu': L['paper'],
            'can': L['metal'], 'tin': L['metal'], 'iron': L['metal'], 'pot': L['metal'], 'tray': L['metal'], 'brass': L['metal']
        }
        
        main_label = decoded[0][1].lower()
        verdict = L['unknown']
        for key, val in mapping.items():
            if key in main_label: 
                verdict = val
                break

        st.markdown('<div class="ai-box">', unsafe_allow_html=True)
        col_img, col_txt = st.columns([1, 1.5], gap="large")
        with col_img: st.image(img, use_container_width=True)
        with col_txt:
            st.markdown(f"<h2 style='margin-top:0;'>{L['verdict']} <span style='color:{accent};'>{verdict}</span></h2>", unsafe_allow_html=True)
            for _, label, prob in decoded:
                st.write(f"**{label.replace('_', ' ').capitalize()}**")
                st.progress(float(prob))
                st.caption(f"Confidence: {round(float(prob*100), 1)}%")
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f"<br><br><p style='text-align:center; opacity:0.2;'>© 2026 {L['name']}</p>", unsafe_allow_html=True)
