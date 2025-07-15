import streamlit as st
from login import verificar_usuario
from modulos.ventas import modulo_ventas

# Inicializar sesión si no existe
for key in ['logged_in', 'usuario', 'nombre_usuario', 'module']:
    if key not in st.session_state:
        st.session_state[key] = None


def menu_principal():
    st.title("🏠 Menú Principal")
    st.subheader(f"Bienvenido, {st.session_state.nombre_usuario} (Usuario: {st.session_state.usuario})")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🛒 Ventas"):
            st.session_state.module = "ventas"
    with col2:
        if st.button("📦 Abastecimiento"):
            st.session_state.module = "abastecimiento"

    st.markdown("---")
    if st.button("🔓 Cerrar sesión"):
        for key in ['logged_in', 'usuario', 'nombre_usuario', 'module']:
            st.session_state[key] = None
        st.success("✅ Sesión cerrada correctamente.")
        st.rerun()

def cargar_modulo():
    if st.session_state.module == "ventas":
        modulo_ventas()
    elif st.session_state.module == "abastecimiento":
        mostrar_abastecimiento()
    else:
        menu_principal()

# Ejecución principal
if not st.session_state.logged_in:
    login()
else:
    cargar_modulo()

