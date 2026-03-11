import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np

# Настройка страницы в стиле Future
st.set_page_config(page_title="Yasir.AI | Future Studio", page_icon="⚡", layout="wide")

# --- ФУТУРИСТИЧНЫЙ ДИЗАЙН ---
st.markdown("""
    <style>
    .main { background-color: #05070a; color: #e0e0e0; font-family: 'Orbitron', sans-serif; }
    
    /* Профиль: Картинка слева, Инфо справа */
    .profile-container {
        display: flex;
        align-items: center;
        gap: 30px;
        padding: 40px;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 30px;
    }
    .profile-pic {
        width: 150px;
        height: 150px;
        border-radius: 20%;
        border: 2px solid #facc15;
        object-fit: cover;
    }
    .info-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; width: 100%; }
    .info-item { background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 12px; border-left: 3px solid #facc15; }
    .info-label { color: #888; font-size: 0.8rem; text-transform: uppercase; }
    .info-value { font-weight: bold; font-size: 1.1rem; color: #fff; }

    /* Видео карточки */
    .video-card {
        background: #111;
        border-radius: 15px;
        padding: 10px;
        border: 1px solid #222;
        transition: 0.3s;
    }
    .video-card:hover { border-color: #facc15; transform: translateY(-5px); }

    /* Табы */
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background: transparent !important;
        border: 1px solid #333 !important;
        border-radius: 10px !important;
        color: #888 !important;
    }
    .stTabs [aria-selected="true"] {
        border-color: #facc15 !important;
        color: #facc15 !important;
        background: rgba(250, 204, 21, 0.1) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ВЕРХНЯЯ ПАНЕЛЬ ---
st.markdown("""
<div class="profile-container">
    <img src="https://img.icons8.com/bubbles/200/cyberpunk-head.png" class="profile-pic">
    <div style="flex-grow: 1;">
        <h1 style="margin:0; color:#facc15;">ИШЕНБЕКОВ ЯСИР</h1>
        <p style="color:#888; margin-bottom: 20px;">Digital Creator & AI Developer</p>
        <div class="info-grid">
            <div class="info-item"><div class="info-label">Локация</div><div class="info-value">Бишкек</div></div>
            <div class="info-item"><div class="info-label">Образование</div><div class="info-value">ЭЭЛ №65</div></div>
            <div class="info-item"><div class="info-label">Стек</div><div class="info-value">Python / AI</div></div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Вкладки
tab1, tab2 = st.tabs(["🚀 МОИ ПРОЕКТЫ", "♻️ NEURAL ANALYZER"])

with tab1:
    st.write("### Видео-портфолио")
    v_col1, v_col2 = st.columns(2)
    
    videos = [
        "https://youtu.be/cRumatSprfI",
        "https://youtu.be/IJQV8EpzCAI",
        "https://youtu.be/nG5uaU0ANJQ",
        "https://youtu.be/KpeUXmTIUuQ",
        "https://youtu.be/aN2W4JRKhTY"
    ]
    
    for i, url in enumerate(videos):
        target_col = v_col1 if i % 2 == 0 else v_col2
        with target_col:
            st.markdown('<div class="video-card">', unsafe_allow_html=True)
            st.video(url)
            st.markdown('</div>', unsafe_allow_html=True)
            st.write("")

with tab2:
    st.markdown("### ♻️ WasteWise Engine")
    uploaded_file = st.file_uploader("Загрузите объект для анализа...", type=["jpg","png","jpeg"])
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, width=400)
        with st.spinner('Считывание нейронами...'):
            # Заглушка модели для быстрой загрузки
            model = tf.keras.applications.MobileNetV2(weights='imagenet')
            proc_img = img.resize((224, 224))
            x = tf.keras.preprocessing.image.img_to_array(proc_img)
            x = np.expand_dims(x, axis=0)
            x = tf.keras.applications.mobilenet_v2.preprocess_input(x)
            preds = model.predict(x)
            decoded = tf.keras.applications.mobilenet_v2.decode_predictions(preds, top=3)[0]
        
        for _, label, prob in decoded:
            st.write(f"**{label}**")
            st.progress(float(prob))

st.markdown("<br><hr><center style='color:#444;'>FUTURE STUDIO v2.0 | 2026</center>", unsafe_allow_html=True)
