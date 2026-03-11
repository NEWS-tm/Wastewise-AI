import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np

# Настройка страницы (чистый минимализм)
st.set_page_config(page_title="Ясир Ишенбеков | Студия", page_icon="🌐", layout="wide")

# --- СТРОГИЙ МИНИМАЛИЗМ И НОТКИ БУДУЩЕГО ---
st.markdown("""
    <style>
    /* Основной фон и шрифт */
    .main { background-color: #080a0d; color: #e0e0e0; font-family: 'Segoe UI', sans-serif; }
    
    /* Убираем отступы Streamlit сверху */
    .block-container { padding-top: 1rem; }

    /* Шапка профиля */
    .profile-container {
        display: flex;
        align-items: center;
        gap: 30px;
        padding: 30px;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 25px;
    }
    .profile-pic {
        width: 120px;
        height: 120px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .info-grid { display: flex; gap: 15px; }
    .info-item { background: rgba(255, 255, 255, 0.04); padding: 10px 15px; border-radius: 8px; border: 1px solid rgba(255, 255, 255, 0.05); }
    .info-label { color: #888; font-size: 0.75rem; text-transform: uppercase; }
    .info-value { font-weight: 600; font-size: 1rem; color: #fff; }

    /* Табы (вкладки) без золота */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border: 1px solid #222 !important;
        border-radius: 8px !important;
        color: #888 !important;
        padding: 8px 16px;
    }
    .stTabs [aria-selected="true"] {
        border-color: #444 !important;
        color: #fff !important;
        background: rgba(255, 255, 255, 0.05) !important;
    }

    /* Видео-карточки (минимализм) */
    .video-card {
        background: #000;
        border-radius: 12px;
        padding: 5px;
        border: 1px solid #1a1a1a;
        margin-bottom: 15px;
    }

    /* Компоновка ИИ: Фото слева, Инфо справа */
    .ai-result-container {
        display: flex;
        gap: 20px;
        align-items: flex-start;
        background: rgba(255, 255, 255, 0.02);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .ai-image-prediction {
        width: 200px; /* Уменьшенный размер фото */
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .ai-info-box { flex-grow: 1; }
    </style>
    """, unsafe_allow_html=True)

# --- ШАПКА ---
st.markdown("""
<div class="profile-container">
    <img src="https://img.icons8.com/bubbles/200/cyberpunk-head.png" class="profile-pic">
    <div style="flex-grow: 1;">
        <h1 style="margin:0; font-size: 2.2rem;">ИШЕНБЕКОВ ЯСИР</h1>
        <div style="margin-top: 15px;" class="info-grid">
            <div class="info-item"><div class="info-label">Локация</div><div class="info-value">Бишкек</div></div>
            <div class="info-item"><div class="info-label">Образование</div><div class="info-value">ЭЭЛ №65</div></div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Вкладки
tab1, tab2 = st.tabs(["🚀 МОИ ПРОЕКТЫ", "♻️ NEURAL ANALYZER"])

with tab1:
    st.write("### Видео-портфолио")
    # Сетка в 3 колонки, чтобы видео были меньше
    v_col1, v_col2, v_col3 = st.columns(3, gap="small")
    
    videos = [
        "https://youtu.be/cRumatSprfI",
        "https://youtu.be/IJQV8EpzCAI",
        "https://youtu.be/nG5uaU0ANJQ",
        "https://youtu.be/KpeUXmTIUuQ",
        "https://youtu.be/aN2W4JRKhTY"
    ]
    
    for i, url in enumerate(videos):
        if i % 3 == 0: target_col = v_col1
        elif i % 3 == 1: target_col = v_col2
        else: target_col = v_col3
        
        with target_col:
            st.markdown('<div class="video-card">', unsafe_allow_html=True)
            st.video(url)
            st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown("### ♻️ Neural Waste Analyzer")
    st.write("Загрузите объект для сканирования нейросетью.")
    
    uploaded_file = st.file_uploader("Выбрать файл", type=["jpg","png","jpeg"], label_visibility="collapsed")
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        
        # Запускаем анализ
        with st.spinner('Считывание...'):
            model = tf.keras.applications.MobileNetV2(weights='imagenet')
            proc_img = img.resize((224, 224))
            x = tf.keras.preprocessing.image.img_to_array(proc_img)
            x = np.expand_dims(x, axis=0)
            x = tf.keras.applications.mobilenet_v2.preprocess_input(x)
            preds = model.predict(x)
            decoded = tf.keras.applications.mobilenet_v2.decode_predictions(preds, top=3)[0]

        # --- КРАСИВЫЙ КОМПАКТНЫЙ ВЫВОД ИИ ---
        st.write("---")
        
        # HTML-контейнер для картинки слева и инфо справа
        st.markdown('<div class="ai-result-container">', unsafe_allow_html=True)
        
        # Используем колонки Streamlit внутри контейнера для правильного отображения картинки
        i_col1, i_col2 = st.columns([1, 2]) # 1 часть картинке, 2 части тексту
        
        with i_col1:
            st.image(img, use_container_width=True) # Картинка слева
        
        with i_col2:
            st.markdown("#### Результаты сканирования:")
            # Вывод названий и прогресс-баров справа
            for _, label, prob in decoded:
                percent = round(prob*100, 1)
                st.write(f"**{label}** — {percent}%")
                st.progress(float(prob))
        
        st.markdown('</div>', unsafe_allow_html=True) # Закрываем контейнер

st.markdown("<br><hr><center style='color:#333; font-size:0.8rem;'>YASIR.STUDIO v3.0 | 2026</center>", unsafe_allow_html=True)
