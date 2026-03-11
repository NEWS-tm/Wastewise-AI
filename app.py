import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np

# --- КОНФИГУРАЦИЯ ---
st.set_page_config(page_title="ИШЕНБЕКОВ ЯСИР", layout="wide")

# Фиксированный Dark Mode
bg, txt, card, brd = "#05070a", "#ffffff", "rgba(255,255,255,0.03)", "rgba(255,255,255,0.08)"
accent = "#3b82f6"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg}; color: {txt}; }}
    .main-card {{ background: {card}; border: 1px solid {brd}; border-radius: 24px; padding: 40px; margin-bottom: 30px; }}
    .video-card {{ border: 1px solid #3a3a3a; border-radius: 16px; overflow: hidden; background: #000; margin-bottom: 20px; }}
    .contact-btn {{ display: inline-block; padding: 12px 28px; border-radius: 12px; font-weight: 600; text-decoration: none; margin-right: 12px; background: {accent}; color: white !important; }}
    .ai-box {{ background: {card}; border: 1px solid {brd}; border-radius: 20px; padding: 30px; }}
    [data-testid="stSidebar"] {{ display: none; }} 
    footer {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown(f"""
<div class="main-card">
    <h1 style="margin:0; font-size: 3.5rem; font-weight: 800; letter-spacing: -2px;">ИШЕНБЕКОВ ЯСИР</h1>
    <p style="opacity: 0.5; font-size: 1.1rem; margin-bottom: 25px;">📍 Бишкек &nbsp;•&nbsp; 🏫 ЭЭЛ №65</p>
    <p style="font-size: 1.25rem; line-height: 1.6; max-width: 850px; opacity: 0.9;">
        Я ученик 8-го класса из Бишкека. Создаю IT-проекты на стыке AI и экологии. 
        Это моя цифровая лаборатория.
    </p>
    <div style="margin-top: 35px;">
        <a href="https://wa.me/996507049" class="contact-btn">WhatsApp</a>
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
    # Выводим только существующие проекты без пустых карточек
    for i, url in enumerate(urls):
        with [c1, c2, c3][i % 3]:
            st.markdown('<div class="video-card">', unsafe_allow_html=True)
            st.video(url)
            st.markdown('</div>', unsafe_allow_html=True)

with tabs[1]:
    st.markdown("<br>", unsafe_allow_html=True)
    up = st.file_uploader("Загрузите фото для анализа нейросетью", type=["jpg","png","jpeg"], label_visibility="collapsed")
    if up:
        img = Image.open(up)
        with st.spinner('Анализ объекта...'):
            model = tf.keras.applications.MobileNetV2(weights='imagenet')
            p_img = img.resize((224, 224))
            x = np.expand_dims(tf.keras.preprocessing.image.img_to_array(p_img), axis=0)
            x = tf.keras.applications.mobilenet_v2.preprocess_input(x)
            preds = model.predict(x)
            decoded = tf.keras.applications.mobilenet_v2.decode_predictions(preds, top=5)[0]

        # --- ПОЛНЫЙ МАППИНГ ВСЕХ КАТЕГОРИЙ ---
        glass_items = ['bottle', 'wine', 'beaker', 'jug', 'vial', 'glass', 'goblet', 'decanter', 'teapot', 'cup']
        plastic_items = ['plastic', 'bag', 'shaker', 'tub', 'soap', 'container', 'water_bottle', 'pill_bottle', 'balloon', 'packet']
        paper_items = ['paper', 'box', 'cardboard', 'envelope', 'packet', 'carton', 'notebook', 'book_jacket', 'menu', 'plate']
        metal_items = ['can', 'tin', 'filter', 'iron', 'pot', 'brass', 'safety_pin', 'ashcan', 'tray', 'bucket', 'hammer']

        verdict = "Анализируем..."
        color = "#9ca3af"
        
        found = False
        for _, label, prob in decoded:
            label = label.lower()
            if any(x in label for x in glass_items): verdict, color = "СТЕКЛО", "#4ade80"; found = True
            elif any(x in label for x in plastic_items): verdict, color = "ПЛАСТИК", "#3b82f6"; found = True
            elif any(x in label for x in paper_items): verdict, color = "БУМАГА / КАРТОН", "#fbbf24"; found = True
            elif any(x in label for x in metal_items): verdict, color = "МЕТАЛЛ", "#f87171"; found = True
            if found: break
        
        # Если ничего не нашли в топ-5, но уверенность высокая - ставим общую категорию
        if not found and decoded[0][2] > 0.1:
            verdict, color = "ПРОЧЕЕ (ТРЕБУЕТ ПРОВЕРКИ)", "#9ca3af"

        st.markdown('<div class="ai-box">', unsafe_allow_html=True)
        col_img, col_txt = st.columns([1, 1.5], gap="large")
        with col_img: st.image(img, use_container_width=True)
        with col_txt:
            st.markdown(f"<h2 style='margin-top:0;'>ВЕРДИКТ: <span style='color:{color};'>{verdict}</span></h2>", unsafe_allow_html=True)
            st.write("---")
            for _, label, prob in decoded:
                name = label.replace('_', ' ').capitalize()
                st.write(f"**{name}**")
                st.progress(float(prob))
                st.caption(f"Точность: {round(float(prob*100), 1)}%")
        st.markdown('</div>', unsafe_allow_html=True)
