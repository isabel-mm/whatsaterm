import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# ---- Interfaz gráfica ----
st.title("Selección de términos en lingüística de corpus")
st.write("Por favor, introduce tu nombre y selecciona términos en el texto.")

# Entrada del nombre del usuario
user_name = st.text_input("Nombre:")

# Texto de ejemplo
texto = """La lingüística de corpus es una metodología que emplea corpus electrónicos para analizar fenómenos lingüísticos con base en datos reales. Se distingue por el uso de herramientas computacionales para identificar patrones y frecuencias léxicas."""

# ---- JavaScript para capturar la selección de texto ----
custom_js = """
<script>
    function getSelectedText() {
        var text = window.getSelection().toString().trim();
        if (text.length > 0) {
            var iframe = parent.document.querySelector('iframe');
            iframe.contentWindow.postMessage(text, '*');
        }
    }
    document.addEventListener("mouseup", getSelectedText);
</script>
"""

components.html(custom_js, height=0)

# ---- Captura la selección usando Streamlit session state ----
if "selected_terms" not in st.session_state:
    st.session_state.selected_terms = []

# ---- Espacio para recibir el término seleccionado ----
selected_text = st.text_input("Texto seleccionado automáticamente:", key="selected_text")

# ---- Función para agregar términos seleccionados ----
if st.button("Marcar término"):
    if selected_text and selected_text not in st.session_state.selected_terms:
        st.session_state.selected_terms.append(selected_text)
        st.experimental_rerun()  # Recargar la página para reflejar cambios

# ---- Mostrar términos seleccionados ----
st.write("### Términos seleccionados:")
if st.session_state.selected_terms:
    for term in st.session_state.selected_terms:
        st.write(f"- {term}")

# ---- Notas del usuario ----
user_notes = st.text_area("Notas u observaciones:")

# ---- Exportar términos a CSV ----
if st.button("Guardar y exportar"):
    if not st.session_state.selected_terms:
        st.error("⚠ No hay términos seleccionados.")
    else:
        data = {
            "Término": st.session_state.selected_terms,
            "Usuario": [user_name] * len(st.session_state.selected_terms),
            "Observaciones": [user_notes] * len(st.session_state.selected_terms),
        }
        df = pd.DataFrame(data)
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📥 Descargar términos seleccionados",
            data=csv,
            file_name="terminos_seleccionados.csv",
            mime="text/csv",
        )

st.write("Cuando termines, envíame el archivo a isabel.moyano@uca.es. ¡Gracias! 😊")
