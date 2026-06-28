import streamlit as st

st.set_page_config(
    page_title="ACB Basketball Analytics",
    page_icon="🏀",
    layout="wide"
)

# Crear la variable de sesión la primera vez
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ----------------------------
# LOGIN
# ----------------------------

if not st.session_state.logged_in:

    st.title("🏀 ACB Basketball Analytics")

    st.subheader("Inicio de sesión")

    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Entrar"):

        if username == "admin" and password == "admin":
            st.session_state.logged_in = True
            st.rerun()

        else:
            st.error("Usuario o contraseña incorrectos.")

# ----------------------------
# APP
# ----------------------------

else:

    st.title("🏀 ACB Basketball Analytics")
    
    st.write(
        """
        Bienvenido a la aplicación de análisis de la Liga Endesa.
    
        Utiliza el menú lateral para acceder a:
        - 🏆 Clasificación
        - 🏀 Partidos
        """
    )
    
    if st.button("Cerrar sesión"):
        st.session_state.logged_in = False
        st.rerun()