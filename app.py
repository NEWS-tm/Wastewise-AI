import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np

# Настройка страницы
st.set_page_config(page_title="Ишенбеков Ясир | Studio", page_icon="🚀", layout="wide")

# --- СТИЛИЗАЦИЯ ПОД ТВОЁ ПОРТФОЛИО ---
st.markdown("""
    <style>
    /* Основной фон как на твоем сайте */
    .main {
        background-color: #0e1117;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    /* Стиль карточек (Город, Школа, Направление) */
    .info-card {
        background-color: #1f2937;
        border-radius: 15px;
        padding: 20px;
        border: 1px solid #374151;
        text-align: left;
    }
    .card-label { color: #facc15; font-size: 0.9rem; font-weight: 600; }
    .card-value { font-size: 1.1rem; font-weight: 700; margin-top: 5px; }
    
    /* Стиль главного описания */
    .bio-box {
        background-color: #1f2937;
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        border: 1px solid #374151;
        line-height: 1.6;
    }
    .highlight { color: #facc15; font-weight: 700; }

    /* Настройка вкладок (Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        justify-content: center;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1f2937;
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        color: white;
    }
    .stTabs [aria-selected="true"] {
        background-color: #facc15 !important;
        color: #000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ВЕРХНЯЯ ЧАСТЬ (КАК НА САЙТЕ) ---
st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>Ишенбеков Ясир</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9ca3af;'>Персональное портфолио</p>", unsafe_allow_html=True)

# Вкладки для навигации без перезагрузки
tab_about, tab_ai = st.tabs(["👤 Обо мне", "♻️ Нейросеть WasteWise"])

with tab_about:
    # Блок с карточками
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="info-card"><div class="card-label">Город:</div><div class="card-value">Бишкек</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="info-card"><div class="card-label">Школа:</div><div class="card-value">ЭЭЛ №65</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="info-card"><div class="card-label">Направление:</div><div class="card-value">IT / Разработка</div></div>', unsafe_allow_html=True)

    # Основной текст
    st.markdown(f"""
    <div class="bio-box">
        Меня зовут <span class="highlight">Ишенбеков Ясир</span>. Я ученик школы <span class="highlight">ЭЭЛ №65</span> из города <span class="highlight">Бишкек</span>. 
        Интересуюсь IT, созданием сайтов и видеопроектами. Постоянно учусь и развиваюсь.
    </div>
    """, unsafe_allow_html=True)
    
    st.write("### Мои работы")
    st.info("Здесь будут отображаться твои проекты, как в нижней части твоего сайта.")

with tab_ai:
    st.header("♻️ WasteWise AI")
    st.write("Загрузи фото мусора, и я определю его тип для правильной переработки.")
    
    uploaded_file = st.file_uploader("Выбери фото...", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, use_container_width=True)
        
        with st.spinner('Анализирую...'):
            # Загрузка легкой модели прямо здесь
            model = tf.keras.applications.MobileNetV2(weights='imagenet')
            img = image.resize((224, 224))
            x = tf.keras.preprocessing.image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = tf.keras.applications.mobilenet_v2.preprocess_input(x)
            
            preds = model.predict(x)
            decoded = tf.keras.applications.mobilenet_v2.decode_predictions(preds, top=3)[0]

        st.success("Готово!")
        for i, (id, label, prob) in enumerate(decoded):
            st.write(f"**{label}**: {round(prob*100, 1)}%")
            st.progress(float(prob))
