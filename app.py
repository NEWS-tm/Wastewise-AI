import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np

# --- КОНФИГУРАЦИЯ ---
st.set_page_config(page_title="ИШЕНБЕКОВ ЯСИР", layout="wide")

# Фиксированные цвета (Только черный/темный стиль)
bg, txt, card, brd = "#05070a", "#ffffff", "rgba(255,255,255,0.03)", "rgba(255,255,255,0.08)"
accent = "#3b82f6"

# --- СТИЛИ ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg}; color: {txt}; }}
    .main-card {{
        background: {card}; border: 1px solid {brd}; border-radius: 24px; padding: 40px; margin-bottom: 30px;
    }}
    .video-card {{
        border: 1px solid #3a3a3a; border-radius: 16px; overflow: hidden; background: #000; margin-bottom: 20px;
    }}
    .soon-card {{
        border: 1px dashed {brd}; border-radius: 16px; height: 210px;
        display: flex; align-items: center; justify-content: center; opacity: 0.4; font-weight: bold;
    }}
    .contact-btn {{
        display: inline-block; padding: 12px 28px; border-radius: 12px; font-weight: 600;
        text-decoration: none; margin-right: 12px; background: {accent}; color: white !important;
    }}
    .ai-box {{ background: {card}; border: 1px solid {brd}; border-radius: 20px; padding: 30px; }}
    </style>
    """, unsafe_allow_html=True)

# --- ШАПКА ---
st.markdown(f"""
<div class="main-card">
    <h1 style="margin:0; font-size: 3.5rem; font-weight: 800; letter-spacing: -2px;">ИШЕНБЕКОВ ЯСИР</h1>
    <p style="opacity: 0.5; font-size: 1.1rem; margin-bottom: 25px;">📍 Бишкек &nbsp;•&nbsp; 🏫 ЭЭЛ №65</p>
    <p style="font-size: 1.25rem; line-height: 1.6; max-width: 850px; opacity: 0.9;">
        Я ученик 8-го класса из Бишкека. Разрабатываю IT-проекты на стыке AI и экологии. 
        Добро пожаловать в мою цифровую лабораторию!
    </p>
    <div style="margin-top: 35px;">
        <a href="https://wa.me/996507049" class="contact-btn">Написать в WhatsApp</a>
        <a href="https://t.me/HewsTM" class="contact-btn" style="background:#0088cc;">Telegram</a>
    </div>
</div>
""", unsafe_allow_html=True)

tabs = st.tabs(["🚀 МОИ ПРОЕКТЫ", "♻️ NEURAL ANALYZER"])

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
            st.markdown('<div class="video-card">', unsafe_allow_html=True)
            st.video(url)
            st.markdown('</div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="soon-card">Скоро будет...</div>', unsafe_allow_html=True)

with tabs[1]:
    st.markdown("<br>", unsafe_allow_html=True)
    up = st.file_uploader("Загрузите фото объекта для анализа нейросетью", type=["jpg","png","jpeg"], label_visibility="collapsed")
    if up:
        img = Image.open(up)
        with st.spinner('Нейросеть WasteWise анализирует...'):
            model = tf.keras.applications.MobileNetV2(weights='imagenet')
            p_img = img.resize((224, 224))
            x = np.expand_dims(tf.keras.preprocessing.image.img_to_array(p_img), axis=0)
            x = tf.keras.applications.mobilenet_v2.preprocess_input(x)
            preds = model.predict(x)
            decoded = tf.keras.applications.mobilenet_v2.decode_predictions(preds, top=3)[0]

        # --- ОБУЧЕНИЕ (Улучшенный маппинг) ---
        mapping = {
            'glass': 'СТЕКЛО', 'bottle': 'СТЕКЛО', 'beaker': 'СТЕКЛО', 'jug': 'СТЕКЛО', 'vial': 'СТЕКЛО',
            'plastic': 'ПЛАСТИК', 'bag': 'ПЛАСТИК', 'wrapper': 'ПЛАСТИК', 'tub': 'ПЛАСТИК',
            'paper': 'БУМАГА / КАРТОН', 'box': 'БУМАГА / КАРТОН', 'cardboard': 'БУМАГА / КАРТОН', 'envelope': 'БУМАГА / КАРТОН',
            'can': 'МЕТАЛЛ', 'tin': 'МЕТАЛЛ', 'filter': 'МЕТАЛЛ', 'pot': 'МЕТАЛЛ', 'ashcan': 'МЕТАЛЛ'
        }
        
        main_label = decoded[0][1].lower()
        verdict = "Не определено"
        for key, val in mapping.items():
            if key in main_label: 
                verdict = val
                break

        st.markdown('<div class="ai-box">', unsafe_allow_html=True)
        col_img, col_txt = st.columns([1, 1.5], gap="large")
        with col_img: st.image(img, use_container_width=True)
        with col_txt:
            st.markdown(f"<h2 style='margin-top:0;'>ВЕРДИКТ: <span style='color:#4ade80;'>{verdict}</span></h2>", unsafe_allow_html=True)
            st.write("---")
            for _, label, prob in decoded:
                st.write(f"**{label.replace('_', ' ').capitalize()}**")
                st.progress(float(prob))
                st.caption(f"Вероятность: {round(float(prob*100), 1)}%")
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br><br><p style='text-align:center; opacity:0.2;'>© 2026 Ишенбеков Ясир. Все права защищены.</p>", unsafe_allow_html=True)
