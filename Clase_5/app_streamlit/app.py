import streamlit as st

st.set_page_config(page_title="Mi app Streamlit", page_icon=":sparkles:")

st.title("Mi primera app con Streamlit")
st.write("Una aplicación mínima para empezar.")

nombre = st.text_input("¿Cómo te llamas?")
color = st.selectbox("Elige un color", ["Azul", "Verde", "Rojo"])

if st.button("Saludar"):
    saludo = nombre.strip() or "visitante"
    st.success(f"Hola, {saludo}. Tu color elegido es {color}.")
