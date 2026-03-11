import streamlit as st

# Настройка страницы
st.set_page_config(page_title="Yasir Ishenbekov Studio", page_icon="🚀", layout="centered")

# --- УЛУЧШЕННЫЙ ДИЗАЙН ---
st.markdown("""
    <style>
    /* Темный фон и шрифт */
    .main {
        background-color: #0e1117;
        color: #ffffff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    /* Центрирование контента */
    .block-container {
        padding-top: 3rem;
        max-width: 700px;
    }
    /* Стиль заголовка */
    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 10px;
        background: -webkit-linear-gradient(#eee, #333);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    /* Текст об авторе */
    .bio-text {
        text-align: center;
        font-size: 18px;
        color: #a0a0a0;
        line-height: 1.6;
        margin-bottom: 40px;
    }
    /* Красивые кнопки */
    div.stButton > button:first-child {
        background-color: #1f2937;
        color: white;
        border: 1px solid #374151;
        border-radius: 12px;
        padding: 20px;
        width: 100%;
        font-size: 18px;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        border-color: #3b82f6;
        color: #3b82f6;
        transform: translateY(-2px);
    }
    /* Ссылка-кнопка */
    .stDownloadButton, .stLinkButton {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- КОНТЕНТ ---
st.markdown('<h1 class="main-title">🚀 Yasir Ishenbekov Studio</h1>', unsafe_allow_html=True)

st.markdown("""
<div class="bio-text">
    Привет! Я <b>Ясир</b>, ученик 8-го класса ЭЭЛ №65. <br>
    Я создаю IT-проекты на стыке искусственного интеллекта и экологии. 
    Добро пожаловать в мою цифровую лабораторию!
</div>
""", unsafe_allow_html=True)

st.write("---")

# Сетка для кнопок
col1, col2 = st.columns(2, gap="medium")

with col1:
    st.link_button("📂 Моё Портфолио", "https://news-tm.github.io/Yasir-Ishenbekov-Studio/", use_container_width=True)

with col2:
    if st.button("♻️ Нейросеть WasteWise", use_container_width=True):
        st.switch_page("pages/classifier.py")

st.write("")
st.write("")
st.divider()
st.caption("© 2026 Yasir Ishenbekov. Разработано в Бишкеке с помощью Python 🐍")
