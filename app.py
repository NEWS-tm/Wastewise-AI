import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# 1. Настройка страницы
st.set_page_config(page_title="Wastewise AI", page_icon="♻️")
st.title("♻️ Wastewise — Умная сортировка")
st.write("Загрузи фото, и ИИ проанализирует детали объекта.")

# 2. Загружаем модель
@st.cache_resource
def get_model():
    return tf.keras.applications.MobileNetV2(weights='imagenet')

model = get_model()

# Словарь категорий
CATEGORIES = {
    'ПЛАСТИК 🔵': ['bottle', 'nipple', 'container', 'cup', 'plastic', 'silicone', 'water_bottle', 'vial'],
    'МЕТАЛЛ 🔴': ['can', 'tin', 'pot', 'iron', 'steel', 'brass', 'metal', 'aluminum'],
    'СТЕКЛО 🟢': ['glass', 'wine_bottle', 'beer_bottle', 'jar', 'beaker', 'flask'],
    'БУМАГА/КАРТОН 🟡': ['envelope', 'paper', 'cardboard', 'carton', 'packet', 'box'],
    'ЭЛЕКТРОНИКА ⚠️': ['laptop', 'mouse', 'keyboard', 'phone', 'computer', 'screen']
}

# 3. Загрузка фото
uploaded_file = st.file_uploader("Выберите изображение...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Объект для анализа', width='stretch')
    
    if st.button('Глубокий анализ деталей'):
        st.write("🔍 Изучаю текстуру и форму...")
        
        # Подготовка фото
        img_resized = image.resize((224, 224))
        img_array = tf.keras.preprocessing.image.img_to_array(img_resized)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)

        # Предсказание
        preds = model.predict(img_array)
        top_3 = tf.keras.applications.mobilenet_v2.decode_predictions(preds, top=3)[0]
        
        st.subheader("Результаты сканирования:")
        
        final_category = None
        
        for i, (id, label, prob) in enumerate(top_3):
            clean_label = label.replace('_', ' ')
            confidence = prob * 100
            st.write(f"{i+1}. **{clean_label}** — уверенность {confidence:.1f}%")
            
            # ИСПРАВЛЕНО: преобразуем prob в обычный float для st.progress
            st.progress(float(prob))
            
            if final_category is None:
                for cat_name, keywords in CATEGORIES.items():
                    if any(key in label.lower() for key in keywords):
                        final_category = cat_name

        st.divider()
        if final_category:
            st.header(f"Итог: {final_category}")
        else:
            st.warning("Тип материала не определен. Попробуй другой ракурс.")