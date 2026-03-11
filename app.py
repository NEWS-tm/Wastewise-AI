import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np

# --- ИНИЦИАЛИЗАЦИЯ СОСТОЯНИЯ ---
if 'theme' not in st.session_state: st.session_state.theme = 'dark'
if 'lang' not in st.session_state: st.session_state.lang = 'RU'

# --- СЛОВАРЬ ПЕРЕВОДА ---
texts = {
    'RU': {
        'title': 'ИШЕНБЕКОВ ЯСИР', 'loc': 'ЛОКАЦИЯ', 'school': 'ШКОЛА', 'city': 'Бишкек',
        'tab1': '🚀 МОИ ПРОЕКТЫ', 'tab2': '♻️ АНАЛИЗАТОР', 'up_msg': 'Загрузить фото',
        'result': 'Результаты:', 'verdict': '🤖 Вердикт:', 'unknown': 'Не определено',
        'glass': 'Стекло', 'plastic': 'Пластик', 'paper': 'Бумага/Картон', 'metal': 'Металл',
        'settings': 'Настройки', 'toggle_theme': '🌓 Тема', 'lang_btn': '🌐 Язык: RU'
    },
    'EN': {
        'title': 'YASIR ISHENBEKOV', 'loc': 'LOCATION', 'school': 'SCHOOL', 'city': 'Bishkek',
        'tab1': '🚀 PROJECTS', 'tab2': '♻️ ANALYZER', 'up_msg': 'Upload photo',
        'result': 'Results:', 'verdict': '🤖 Verdict:', 'unknown': 'Unknown',
        'glass': 'Glass', 'plastic': 'Plastic', 'paper': 'Paper/Cardboard', 'metal': 'Metal',
        'settings': 'Settings', 'toggle_theme': '🌓 Theme', 'lang_btn': '🌐 Lang: EN'
    }
}

L = texts[st.session_state.lang]

# --- ФУНКЦИИ ---
def toggle_theme(): st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
def toggle_lang(): st.session_state.lang = 'EN' if st.session_state.lang == 'RU' else 'RU'

# Боковая панель
with st.sidebar:
    st.markdown(f"### {L['settings']}")
    if st.button(L['toggle_theme'], use_container_width=True): toggle_theme()
    if st.button(L['lang_btn'], use_container_width=True): toggle_lang()

# Конфиг
st.set_page_config(page_title=L['title'], layout="wide")

# Цвета
if st.session_state.theme == 'dark':
    bg, txt, card = "#080a0d", "#e0e0e0", "rgba(255,255,255,0.03)"
    brd = "rgba(255,255,255,0.1)"
else:
    bg, txt, card = "#ffffff", "#1a1a1a", "#f0f2f6"
    brd = "#d1d5db"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg}; color: {txt}; }}
    .profile-container {{ padding: 25px; background: {card}; border-radius: 15px; border: 1px solid {brd}; margin-bottom: 25px; }}
    .info-item {{ background: {card}; padding: 10px 20px; border-radius: 8px; border: 1px solid {brd}; }}
    .video-card {{ background: {card}; border-radius: 12px; padding: 10px; border: 1px solid {brd}; }}
    .ai-box {{ background: {card}; padding: 20px; border-radius: 12px; border: 1px solid {brd}; display: flex; gap: 20px; }}
    </style>
    """, unsafe_allow_html=True)

# --- ШАПКА ---
st.markdown(f"""
<div class="profile-container">
    <h1 style="margin:0; font-size: 2.5rem;">{L['title']}</h1>
    <div style="margin-top: 15px; display: flex; gap: 15px;">
        <div class="info-item"><span style="color:#888; font-size:0.7rem;">{L['loc']}:</span><br><b>{L['city']}</b></div>
        <div class="info-item"><span style="color:#888; font-size:0.8rem;">{L['school']}:</span><br><b>ЭЭЛ №65</b></div>
    </div>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs([L['tab1'], L['tab2']])

with tab1:
    v_col1, v_col2, v_col3 = st.columns(3)
    v_urls = ["https://youtu.be/cRumatSprfI", "https://youtu.be/IJQV8EpzCAI", "https://youtu.be/nG5uaU0ANJQ", "https://youtu.be/KpeUXmTIUuQ", "https://youtu.be/aN2W4JRKhTY"]
    for i, url in enumerate(v_urls):
        with [v_col1, v_col2, v_col3][i % 3]:
            st.markdown('<div class="video-card">', unsafe_allow_html=True); st.video(url); st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    up_file = st.file_uploader(L['up_msg'], type=["jpg","png","jpeg"], label_visibility="collapsed")
    if up_file:
        img = Image.open(up_file)
        with st.spinner('AI...'):
            model = tf.keras.applications.MobileNetV2(weights='imagenet')
            p_img = img.resize((224, 224))
            x = tf.keras.preprocessing.image.img_to_array(p_img)
            x = np.expand_dims(x, axis=0)
            x = tf.keras.applications.mobilenet_v2.preprocess_input(x)
            preds = model.predict(x)
            decoded = tf.keras.applications.mobilenet_v2.decode_predictions(preds, top=3)[0]

        # Логика распознавания (обучение через маппинг)
        mapping = {
            'glass': L['glass'], 'bottle': L['glass'], 'wine': L['glass'], 'beaker': L['glass'],
            'plastic': L['plastic'], 'bag': L['plastic'], 'container': L['plastic'], 'wrapper': L['plastic'],
            'paper': L['paper'], 'box': L['paper'], 'cardboard': L['paper'], 'envelope': L['paper'],
            'can': L['metal'], 'tin': L['metal'], 'metal': L['metal'], 'aluminum': L['metal']
        }
        
        main_label = decoded[0][1].lower()
        verdict = L['unknown']
        for key in mapping:
            if key in main_label: verdict = mapping[key]

        st.markdown('<div class="ai-box">', unsafe_allow_html=True)
        c1, c2 = st.columns([1, 2])
        with c1: st.image(img, use_container_width=True)
        with c2:
            st.write(f"#### {L['result']}")
            for _, label, prob in decoded:
                st.write(f"**{label}**: {round(float(prob*100), 1)}%")
                st.progress(float(prob))
            st.success(f"{L['verdict']} **{verdict}**")
        st.markdown('</div>', unsafe_allow_html=True)
