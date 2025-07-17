import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'modulos'))

import streamlit as st
from login import login, verificar_usuario
from modulos.ventas import modulo_ventas
from modulos.compras import modulo_compras

def menu_principal():
    st.title("🏠 Menú Principal")

    # Aquí usamos el nombre del empleado en lugar del "usuario"
    nombre_empleado = st.session_state.get("nombre_empleado", "Usuario")  # Cambiado para usar 'nombre_empleado'
    st.subheader(f"Bienvenido, {nombre_empleado}")  # Mostrar el nombre del empleado

    # Opciones del menú
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🛒 Ventas"):
            st.session_state.module = "Ventas"
            st.rerun()
            
    with col2:
        if st.button("📥 Compras"):
            st.session_state.module = "Compras"
            st.rerun()

    with col3:
        if st.button("📦 Inventario"):
            st.session_state.module = "Inventario"
            st.rerun()

    st.markdown("---")
    if st.button("🔓 Cerrar sesión"):
        # Limpiar las claves de sesión relacionadas con el usuario
        for key in ['logueado', 'usuario', 'module', 'nombre_empleado']:  # También eliminar 'nombre_empleado'
            if key in st.session_state:
                del st.session_state[key]
        st.success("✅ Sesión cerrada correctamente.")
        st.rerun()

def cargar_modulo():
    if "module" in st.session_state:
        if st.session_state.module == "Ventas":
            modulo_ventas()
        elif st.session_state.module == "Compras":
            modulo_compras()
        elif st.session_state.module == "Inventario":
            st.write("🔧 Módulo de inventario en construcción...")
        else:
            menu_principal()
    else:
        menu_principal()

def app():
    # Verifica si el usuario está logueado
    if "logueado" not in st.session_state or not st.session_state["logueado"]:
        login()  # Si no está logueado, mostrar login
    else:
        cargar_modulo()  # Si está logueado, cargar el módulo correspondiente

if __name__ == "__main__":
    app()
