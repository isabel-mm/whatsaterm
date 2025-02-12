import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# ---- Configuración inicial ----
st.title("Selección de términos en lingüística de corpus")
st.write("Selecciona términos directamente en el texto y haz clic en 'Marcar término' para guardarlos.")

# Entrada del nombre del usuario
user_name = st.text_input("Nombre:")

# ---- Definir el texto a analizar ----
texto = """La lingüística de corpus es una metodología que emplea corpus electrónicos para analizar fenómenos lingüísticos con base en datos reales. Se distingue por el uso de herramientas computacionales para identificar patrones y frecuencias léxicas."""

# ---- Estado de sesión para almacenar términos seleccionados ----
if "selected_terms" not in st.session_state:
    st.session_state.selected_terms = []

# ---- Mostrar el texto en pantalla ----
st.write("### Texto:")
st.markdown(f"<div id='texto' style='border:1px solid gray; padding:10px;'>{texto}</div>", unsafe_allow_html=True)

# ---- JavaScript para capturar la selección de texto ----
custom_js = """
<script>
    function sendSelectionToStreamlit() {
        var selectedText = window.getSelection().toString().trim();
        if (selectedText.length > 0) {
            var streamlitInput = window.parent.document.querySelector('input[data-testid="stTextInput"]');
            if (streamlitInput) {
                streamlitInput.value = selectedText;
                streamlitInput.dispatchEvent(new Event('input', { bubbles: true }));
            }
        }
    }
    document.addEventListener("mouseup", sendSelectionToStreamlit);
</script>
"""

components.html(custom_js, height=0)

# ---- Espacio donde se guarda la selección de texto ----
selected_text = st.text_input("Texto seleccionado automáticamente:", key="selected_text")

# ---- Botón para marcar el término ----
if st.button("Marcar término"):
    if selected_text and selected_text not in st.session_state.selected_terms:
        st.session_state.selected_terms.append(selected_text)

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
