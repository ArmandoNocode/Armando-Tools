import streamlit as st
import pandas as pd
import io

# --- CONFIGURACIÓN VISUAL ---
st.set_page_config(page_title="Unificador de Excel", page_icon="📊")

st.title("📊 Unificador de Excel Pro")
st.markdown("### Une múltiples archivos en uno solo al instante.")

st.info("Sube tus archivos Excel, nosotros los combinamos y tú descargas el resultado. 100% Gratis.")

# --- ZONA DE CARGA ---
archivos_subidos = st.file_uploader("Arrastra tus archivos Excel aquí (.xlsx)", 
                                  accept_multiple_files=True, 
                                  type=['xlsx'])

if archivos_subidos:
    st.success(f"📂 Has cargado {len(archivos_subidos)} archivos.")
    
    if st.button("🧩 Unir Archivos Ahora"):
        try:
            lista_datos = []
            barra = st.progress(0)
            
            for i, archivo in enumerate(archivos_subidos):
                df = pd.read_excel(archivo)
                lista_datos.append(df)
                barra.progress((i + 1) / len(archivos_subidos))
            
            df_final = pd.concat(lista_datos, ignore_index=True)
            
            st.write("### ✅ Vista previa:")
            st.dataframe(df_final.head(5))
            
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                df_final.to_excel(writer, index=False)
                
            st.download_button(
                label="📥 Descargar Excel Unido",
                data=buffer,
                file_name="Excel_Maestro.xlsx",
                mime="application/vnd.ms-excel"
            )
            
        except Exception as e:
            st.error(f"Error: {e}")
            