import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np

# --- НАСТРОЙКА ТЕМЫ ---
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

def toggle_theme():
    st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'

# Боковая панель для настроек
with st.sidebar:
    st.title("Настройки")
    if st.button("🌓 Сменить тему (Светлая/Темная)"):
        toggle_theme()

# Конфигурация страницы
st.set_page_config(page_title="Ясир Ишенбеков", layout="wide")

# Цвета в зависимости от темы
if st.session_state.theme == 'dark':
    bg_color, text_color, card_bg = "#080a0d", "#e0e0e0", "rgba(255, 255, 255, 0.03)"
    border_color = "rgba(255, 255, 255, 0.1)"
else:
    bg_color, text_color, card_bg = "#ffffff", "#1a1a1a", "#f0f2f6"
    border_color = "#d1d5db"

# --- СТИЛИ ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color}; color: {text_color}; }}
    .profile-container {{
        padding: 25px;
        background: {card_bg};
        border-radius: 15px;
        border: 1px solid {border_color};
        margin-bottom: 25px;
    }}
    .info-item {{ background: {card_bg}; padding: 10px 20px; border-radius: 8px; border: 1px solid {border_color}; }}
    .ai-result-box {{
        display: flex; gap: 25px; align-items: flex-start;
        background: {card_bg}; padding: 20px; border-radius: 12px; border: 1px solid {border_color};
    }}
    .video-card {{ background: {card_bg}; border-radius: 12px; padding: 10px; border: 1px solid {border_color}; }}
    </style>
    """, unsafe_allow_html=True)

# --- ШАПКА (БЕЗ ФОТО) ---
st.markdown(f"""
<div class="profile-container">
    <h1 style="margin:0; font-size: 2.5rem; color: {text_color};">ИШЕНБЕКОВ ЯСИР</h1>
    <div style="margin-top: 15px; display: flex; gap: 15px;">
        <div class="info-item"><span style="color:#888; font-size:0.8rem;">ЛОКАЦИЯ:</span><br><b>Бишкек</b></div>
        <div class="info-item"><span style="color:#888; font-size:0.8rem;">ШКОЛА:</span><br><b>ЭЭЛ №65</b></div>
    </div>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🚀 МОИ ПРОЕКТЫ", "♻️ NEURAL ANALYZER"])

with tab1:
    st.write("### Видео-портфолио")
    v_col1, v_col2, v_col3 = st.columns(3)
    videos = [
        "https://youtu.be/cRumatSprfI", "https://youtu.be/IJQV8EpzCAI",
        "https://youtu.be/nG5uaU0ANJQ", "https://youtu.be/KpeUXmTIUuQ",
        "https://youtu.be/aN2W4JRKhTY"
    ]
    for i, url in enumerate(videos):
        cols = [v_col1, v_col2, v_col3]
        with cols[i % 3]:
            st.markdown('<div class="video-card">', unsafe_allow_html=True)
            st.video(url)
            st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown("### ♻️ Анализатор мусора")
    up_file = st.file_uploader("Загрузить фото", type=["jpg","png","jpeg"], label_visibility="collapsed")
    
    if up_file:
        img = Image.open(up_file)
        with st.spinner('Нейросеть думает...'):
            model = tf.keras.applications.MobileNetV2(weights='imagenet')
            p_img = img.resize((224, 224))
            x = tf.keras.preprocessing.image.img_to_array(p_img)
            x = np.expand_dims(x, axis=0)
            x = tf.keras.applications.mobilenet_v2.preprocess_input(x)
            preds = model.predict(x)
            decoded = tf.keras.applications.mobilenet_v2.decode_predictions(preds, top=3)[0]

        st.markdown('<div class="ai-result-box">', unsafe_allow_html=True)
        c1, c2 = st.columns([1, 2])
        with c1:
            st.image(img, use_container_width=True)
        with c2:
            st.write("#### Результаты:")
            # Словарь для перевода (базовый пример)
            translate = {"beaker": "Стекло", "bottle": "Пластик/Стекло", "box": "Картон", "can": "Металл"}
            
            main_label = decoded[0][1].lower()
            verdict = "Не определено"
            
            for key in translate:
                if key in main_label: verdict = translate[key]

            for _, label, prob in decoded:
                clean_prob = round(float(prob * 100), 1) # Округление до 6.7
                st.write(f"**{label}**: {clean_prob}%")
                st.progress(float(prob))
            
            st.success(f"🤖 Вердикт: **{verdict}**")
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br><center style='opacity:0.5;'>YASIR.STUDIO v4.0</center>", unsafe_allow_html=True)
