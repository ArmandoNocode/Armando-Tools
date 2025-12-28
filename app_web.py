import streamlit as st
import pandas as pd
import io
import os

# --- CONFIGURACIÓN VISUAL ---
st.set_page_config(page_title="Consolidador de Excel", page_icon="📑")

st.title("📑 Consolidador de Excel (Por Hojas)")
st.markdown("### Une archivos Excel en un solo libro con pestañas limpias.")

# --- BARRA LATERAL (OPCIONES) ---
with st.sidebar:
    st.header("⚙️ Configuración")
    st.info("Usa esto si tus Excel tienen títulos o logos arriba de la tabla.")
    # El usuario elige cuántas filas saltar
    filas_a_saltar = st.number_input(
        "Filas a saltar antes del encabezado:", 
        min_value=0, 
        max_value=10, 
        value=0,
        help="Si tu Excel tiene un título en la fila 1 y 2, pon un 2 aquí."
    )

# --- ZONA DE CARGA ---
st.write("---")
archivos_subidos = st.file_uploader("Arrastra tus archivos aquí (.xlsx)", 
                                  accept_multiple_files=True, 
                                  type=['xlsx'])

if archivos_subidos:
    st.success(f"📂 Has cargado {len(archivos_subidos)} archivos.")
    
    if st.button("📚 Crear Libro Maestro"):
        try:
            buffer = io.BytesIO()
            
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                barra = st.progress(0)
                
                for i, archivo in enumerate(archivos_subidos):
                    # --- LA CORRECCIÓN MÁGICA ---
                    # Usamos 'skiprows' con el número que pusiste en la barra lateral
                    df = pd.read_excel(archivo, skiprows=filas_a_saltar)
                    
                    # Limpieza extra: Eliminamos columnas que sean totalmente vacías
                    df = df.dropna(axis=1, how='all')
                    
                    # Nombre de la hoja
                    nombre_hoja = os.path.splitext(archivo.name)[0][:31]
                    
                    # Escribir hoja
                    df.to_excel(writer, sheet_name=nombre_hoja, index=False)
                    
                    barra.progress((i + 1) / len(archivos_subidos))
            
            st.balloons()
            st.success("✅ ¡Listo! Archivo limpio generado.")
            
            st.download_button(
                label="📥 Descargar Excel Limpio",
                data=buffer,
                file_name="Libro_Maestro_Limpio.xlsx",
                mime="application/vnd.ms-excel"
            )
            
        except Exception as e:
            st.error(f"Error: {e}")