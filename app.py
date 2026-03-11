import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np

# --- ИНИЦИАЛИЗАЦИЯ ---
if 'theme' not in st.session_state: st.session_state.theme = 'dark'
if 'lang' not in st.session_state: st.session_state.lang = 'RU'

# --- СЛОВАРЬ ПЕРЕВОДА И ОБУЧЕНИЯ ---
texts = {
    'RU': {
        'name': 'ИШЕНБЕКОВ ЯСИР', 'city': 'Бишкек', 'school': 'ЭЭЛ №65',
        'about': 'Я ученик 8-го класса из города Бишкек. Создаю IT-проекты на стыке AI и экологии. Постоянно развиваюсь и собираю своё цифровое портфолио.',
        'projects': '🚀 МОИ ПРОЕКТЫ', 'analyzer': '♻️ NEURAL WASTE AI',
        'verdict': '🤖 ВЕРДИКТ:', 'unknown': 'Не определено',
        'glass': 'СТЕКЛО', 'plastic': 'ПЛАСТИК', 'paper': 'БУМАГА / КАРТОН', 'metal': 'МЕТАЛЛ',
        'contact_me': 'СВЯЗАТЬСЯ:', 'upload': 'Выберите фото для анализа...'
    },
    'EN': {
        'name': 'YASIR ISHENBEKOV', 'city': 'Bishkek', 'school': 'EEL No. 65',
        'about': '8th-grade student from Bishkek. Creating IT projects focused on AI and ecology. Constantly learning and building my digital portfolio.',
        'projects': '🚀 MY PROJECTS', 'analyzer': '♻️ NEURAL WASTE AI',
        'verdict': '🤖 VERDICT:', 'unknown': 'Unknown',
        'glass': 'GLASS', 'plastic': 'PLASTIC', 'paper': 'PAPER / CARDBOARD', 'metal': 'METAL',
        'contact_me': 'CONTACT:', 'upload': 'Choose a photo to analyze...'
    }
}

L = texts[st.session_state.lang]

# --- КОНФИГУРАЦИЯ ---
st.set_page_config(page_title=L['name'], layout="wide")

# Цветовая схема
if st.session_state.theme == 'dark':
    bg, txt, card, brd = "#0d1117", "#f0f6fc", "rgba(255,255,255,0.05)", "rgba(255,255,255,0.1)"
else:
    bg, txt, card, brd = "#ffffff", "#1a1a1a", "#f6f8fa", "#d0d7de"

# --- СТИЛИ ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg}; color: {txt}; }}
    .profile-card {{
        background: {card}; border: 1px solid {brd}; border-radius: 20px; padding: 40px; margin-bottom: 25px;
    }}
    .video-container {{
        border: 2px solid #000000; /* ЧЕРНАЯ ОБВОДКА */
        border-radius: 12px; overflow: hidden; background: #000; margin-bottom: 20px;
    }}
    .contact-link {{
        display: inline-block; padding: 12px 25px; background: #238636; color: white !important;
        border-radius: 10px; text-decoration: none; font-weight: bold; margin-right: 10px; transition: 0.3s;
    }}
    .contact-link.tg {{ background: #0088cc; }}
    .contact-link:hover {{ opacity: 0.8; transform: translateY(-2px); }}
    .ai-result {{ background: {card}; border-radius: 15px; border: 1px solid {brd}; padding: 25px; }}
    </style>
    """, unsafe_allow_html=True)

# --- БОКОВАЯ ПАНЕЛЬ ---
with st.sidebar:
    st.markdown("### UI SETTINGS")
    if st.button("🌓 Сменить тему", use_container_width=True):
        st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
        st.rerun()
    if st.button("🌐 RU / EN", use_container_width=True):
        st.session_state.lang = 'EN' if st.session_state.lang == 'RU' else 'RU'
        st.rerun()

# --- ОСНОВНОЙ БЛОК ---
st.markdown(f"""
<div class="profile-card">
    <h1 style="margin:0; font-size: 3rem; letter-spacing: -1px;">{L['name']}</h1>
    <p style="opacity: 0.6; font-size: 1.1rem; margin-top: 5px;">📍 {L['city']} | 🏫 {L['school']}</p>
    <p style="margin-top: 20px; font-size: 1.2rem; line-height: 1.6; max-width: 800px;">{L['about']}</p>
    <div style="margin-top: 30px;">
        <span style="display:block; margin-bottom:10px; font-weight:bold; opacity:0.7;">{L['contact_me']}</span>
        <a href="https://wa.me/996507049" class="contact-link">WhatsApp</a>
        <a href="https://t.me/HewsTM" class="contact-link tg">Telegram</a>
    </div>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs([L['projects'], L['analyzer']])

with tab1:
    v_col1, v_col2, v_col3 = st.columns(3)
    urls = [
        "https://youtu.be/cRumatSprfI", "https://youtu.be/IJQV8EpzCAI",
        "https://youtu.be/nG5uaU0ANJQ", "https://youtu.be/KpeUXmTIUuQ",
        "https://youtu.be/aN2W4JRKhTY"
    ]
    for i, url in enumerate(urls):
        with [v_col1, v_col2, v_col3][i % 3]:
            st.markdown('<div class="video-container">', unsafe_allow_html=True)
            st.video(url)
            st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    up = st.file_uploader(L['upload'], type=["jpg","png","jpeg"], label_visibility="collapsed")
    if up:
        img = Image.open(up)
        with st.spinner('🧠 Анализ нейросетью...'):
            model = tf.keras.applications.MobileNetV2(weights='imagenet')
            p_img = img.resize((224, 224))
            x = np.expand_dims(tf.keras.preprocessing.image.img_to_array(p_img), axis=0)
            x = tf.keras.applications.mobilenet_v2.preprocess_input(x)
            preds = model.predict(x)
            decoded = tf.keras.applications.mobilenet_v2.decode_predictions(preds, top=3)[0]

        # --- СУПЕР ОБУЧЕНИЕ (МАППИНГ) ---
        mapping = {
            'glass': L['glass'], 'bottle': L['glass'], 'wine': L['glass'], 'beaker': L['glass'], 'jug': L['glass'],
            'plastic': L['plastic'], 'bag': L['plastic'], 'container': L['plastic'], 'wrapper': L['plastic'], 'tub': L['plastic'],
            'paper': L['paper'], 'box': L['paper'], 'cardboard': L['paper'], 'envelope': L['paper'], 'packet': L['paper'],
            'can': L['metal'], 'tin': L['metal'], 'pot': L['metal'], 'iron': L['metal'], 'filter': L['metal']
        }
        
        main_label = decoded[0][1].lower()
        verdict = L['unknown']
        for key, val in mapping.items():
            if key in main_label: verdict = val

        st.markdown('<div class="ai-result">', unsafe_allow_html=True)
        c1, c2 = st.columns([1, 1.5])
        with c1: st.image(img, use_container_width=True)
        with c2:
            st.subheader(f"{L['verdict']} {verdict}")
            for _, label, prob in decoded:
                st.write(f"**{label}**: {round(float(prob*100), 1)}%")
                st.progress(float(prob))
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br><br><center style='opacity:0.2;'>© 2026 Ishenbekov Yasir</center>", unsafe_allow_html=True)
