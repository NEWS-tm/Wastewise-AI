import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np

# Настройка страницы
st.set_page_config(page_title="WasteWise AI", page_icon="♻️")

# Кнопка возврата на главную Студию
if st.button("⬅️ Назад в Студию"):
    st.switch_page("app.py")

st.title("♻️ WasteWise AI Классификатор")
st.write("Загрузите фото отходов, чтобы нейросеть определила их тип.")

uploaded_file = st.file_uploader("Выберите изображение...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Загруженное фото', use_container_width=True)
    
    with st.spinner('Нейросеть анализирует...'):
        # Используем предобученную модель MobileNetV2
        model = tf.keras.applications.MobileNetV2(weights='imagenet')
        
        img = image.resize((224, 224))
        x = tf.keras.preprocessing.image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = tf.keras.applications.mobilenet_v2.preprocess_input(x)
        
        preds = model.predict(x)
        decoded = tf.keras.applications.mobilenet_v2.decode_predictions(preds, top=3)[0]

    st.success("Анализ завершен!")
    st.subheader("Результаты:")
    for i, (id, label, prob) in enumerate(decoded):
        percent = round(prob * 100, 2)
        st.write(f"**{label}** — {percent}%")
        st.progress(int(percent))
