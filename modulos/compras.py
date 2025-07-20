import streamlit as st
from datetime import datetime
from config.conexion import obtener_conexion

def modulo_compras():
    st.title("🧾 Módulo de Compras")

    # Conectar a la base de datos
    conn = obtener_conexion()
    cursor = conn.cursor()

    # Obtener productos disponibles
    cursor.execute("SELECT Cod_barra, Nombre, Precio_venta FROM Producto")
    productos = cursor.fetchall()

    if not productos:
        st.warning("⚠️ No hay productos disponibles.")
        return

    # Inicializar variables en session_state
    if "productos_seleccionados" not in st.session_state:
        st.session_state["productos_seleccionados"] = []
    if "editar_indice" not in st.session_state:
        st.session_state["editar_indice"] = None


    producto = {}

    # Ingresar código de barras para buscar el producto
    codigo_barras = st.text_input("Código de barras del producto")

    if codigo_barras:
        # Buscar producto por código de barras
        producto_encontrado = None
        for prod in productos:
            if prod[0] == codigo_barras:
                producto_encontrado = prod
                break

        if producto_encontrado:
            producto["cod_barra"] = producto_encontrado[0]
            producto["nombre"] = producto_encontrado[1]
            producto["precio_venta"] = producto_encontrado[2]
            st.write(f"Producto encontrado: **{producto['nombre']}**")
        else:
            st.warning("⚠️ Producto no encontrado. Verifique el código de barras.")

    # Definir valores predeterminados para el precio de compra si no se está editando un producto
    if st.session_state["editar_indice"] is not None:
        producto_edit = st.session_state["productos_seleccionados"][st.session_state["editar_indice"]]
        default_precio_compra = float(producto_edit["precio_compra"])  # Se obtiene el precio del producto editado
    else:
        default_precio_compra = 0.01  # Valor por defecto en caso de nuevo producto

    # Si se encuentra un producto, permite ingresar datos adicionales
    if producto.get("cod_barra"):
        # Ingresar precio de compra (ajustado a no ser menor a 0.01)
        producto["precio_compra"] = st.number_input(
            "Precio de compra",
            min_value=0.01,
            step=0.01,
            value=max(0.01, default_precio_compra)  # Asegura que el valor no sea menor que 0.01
        )

        # Unidad de compra (irá a columna 'unidad' en la tabla productoxcompra)
        unidades_disponibles = ["libra", "kg", "unidad", "docena"]
        producto["unidad"] = st.selectbox(
            "Unidad de compra",
            unidades_disponibles,
            index=0
        )

        # Cantidad como entero
        producto["cantidad"] = st.number_input(
            "Cantidad comprada",
            min_value=1,
            max_value=10000,
            step=1,
            value=1
        )

        # Botón para guardar producto
        if st.button("💾 Agregar producto"):
            st.session_state["productos_seleccionados"].append(producto)
            st.success("✅ Producto agregado a la compra.")

    # Mostrar tabla de productos seleccionados
    if st.session_state["productos_seleccionados"]:
        st.subheader("📦 Productos en la compra actual")

        for i, prod in enumerate(st.session_state["productos_seleccionados"]):
            st.markdown(
                f"**{prod['nombre']}** — {prod['cantidad']} {prod['unidad']} — Precio compra: ${prod['precio_compra']:.2f}"
            )
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button(f"✏️ Editar #{i+1}", key=f"editar_{i}"):
                    st.session_state["editar_indice"] = i
                    st.rerun()
            with col2:
                if st.button(f"❌ Eliminar #{i+1}", key=f"eliminar_{i}"):
                    st.session_state["productos_seleccionados"].pop(i)
                    st.success("🗑️ Producto eliminado.")
                    st.rerun()

    # Botón para guardar toda la compra (se necesita ID de compra)
    st.divider()
    st.subheader("📥 Finalizar compra")


    if st.button("✅ Registrar compra en la base de datos"):
        if not st.session_state["productos_seleccionados"]:
            st.error("❌ No hay productos agregados.")
        else:
            try:
                # Insertar productos en la base de datos
                for prod in st.session_state["productos_seleccionados"]:
                    cursor.execute(
                        "INSERT INTO productoxcompra (id_compra, cod_barra, cantidad, precio_compra, unidad) VALUES (%s, %s, %s, %s, %s)",
                        (id_compra, prod["cod_barra"], prod["cantidad"], prod["precio_compra"], prod["unidad"])
                    )
                conn.commit()
                st.success("📦 Compra registrada exitosamente.")
                st.session_state["productos_seleccionados"] = []
            except Exception as e:
                st.error(f"⚠️ Error al guardar en la base de datos: {e}")

