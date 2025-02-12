import streamlit as st
import pandas as pd

# ---- Interfaz gráfica ----
st.title("Selección de términos en lingüística de corpus")
st.write("Por favor, introduce tu nombre y selecciona términos del texto.")

# Entrada del nombre del usuario
user_name = st.text_input("Nombre:")

# Texto de ejemplo
texto = """La lingüística de corpus es una metodología que emplea corpus electrónicos para analizar fenómenos lingüísticos con base en datos reales. Se distingue por el uso de herramientas computacionales para identificar patrones y frecuencias léxicas."""
st.write(texto)

# Selección de términos
terms = st.multiselect("Selecciona los términos importantes", texto.split())

# Notas del usuario
user_notes = st.text_area("Notas u observaciones:")

# Exportar términos a CSV
if st.button("Guardar y exportar"):
    if not terms:
        st.error("⚠ No hay términos seleccionados.")
    else:
        data = {"Término": terms, "Usuario": user_name, "Observaciones": user_notes}
        df = pd.DataFrame(data)
        
        # Convertir a CSV
        csv = df.to_csv(index=False).encode("utf-8")
        
        # Botón de descarga
        st.download_button(
            label="📥 Descargar términos seleccionados",
            data=csv,
            file_name="terminos_seleccionados.csv",
            mime="text/csv",
        )

st.write("Cuando termines, envíame el archivo a isabel.moyano@uca.es. ¡Gracias! 😊")
