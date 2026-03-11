import streamlit as st

# Настройка страницы в стиле твоей студии
st.set_page_config(page_title="Yasir Ishenbekov Studio", page_icon="🚀", layout="centered")

# Применяем темную тему и стильные кнопки
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: white;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3.5em;
        background-color: #2e7bcf;
        color: white;
        border: none;
        font-weight: bold;
        font-size: 18px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #1c5a9e;
        transform: scale(1.02);
    }
    .bio-container {
        text-align: center;
        padding: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Контент страницы
st.markdown('<div class="bio-container">', unsafe_allow_html=True)
st.title("🚀 Yasir Ishenbekov Studio")
st.write("### Привет! Я Ясир, ученик 8-го класса ЭЭЛ №65.")
st.write("Я увлекаюсь программированием на Python и создаю AI-решения для экологии. Добро пожаловать в мой цифровой мир!")
st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# Кнопки навигации
col1, col2 = st.columns(2)

with col1:
    # Ссылка на твой старый сайт-портфолио (про хлеб и семью)
    st.link_button("📂 Моё Портфолио", "https://news-tm.github.io/Yasir-Ishenbekov-Studio/")

with col2:
    # Переход на страницу с нейросетью
    if st.button("♻️ Распознавание мусора"):
        st.switch_page("pages/classifier.py")

st.divider()
st.caption("© 2026 Yasir Ishenbekov. Создано с помощью Streamlit и TensorFlow.")
