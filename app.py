import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# ---- Configuración inicial ----
st.title("Selección de términos en lingüística de corpus")
st.write("Selecciona términos directamente en el texto para marcarlos.")

# Entrada del nombre del usuario
user_name = st.text_input("Nombre:")

# ---- Definir el texto a analizar ----
texto = """La lingüística de corpus es una metodología que emplea corpus electrónicos para analizar fenómenos lingüísticos con base en datos reales. Se distingue por el uso de herramientas computacionales para identificar patrones y frecuencias léxicas."""

# ---- Estado de sesión para almacenar términos seleccionados ----
if "selected_terms" not in st.session_state:
    st.session_state.selected_terms = []

# ---- JavaScript para capturar automáticamente la selección de texto ----
custom_js = """
<script>
    document.addEventListener("mouseup", function() {
        var selectedText = window.getSelection().toString().trim();
        if (selectedText.length > 0) {
            var streamlitInput = window.parent.document.querySelector('input[data-testid="stTextInput"]');
            if (streamlitInput) {
                streamlitInput.value = selectedText;
                streamlitInput.dispatchEvent(new Event('input', { bubbles: true }));
            }
        }
    });
</script>
"""

components.html(custom_js, height=0)

# ---- Campo oculto donde se recibe la selección ----
selected_text = st.text_input("Texto seleccionado automáticamente:", key="selected_text")

# ---- Guardar la selección sin hacer clic en ningún botón ----
if selected_text and selected_text not in st.session_state.selected_terms:
    st.session_state.selected_terms.append(selected_text)
    st.experimental_rerun()  # Recargar la página para reflejar los cambios inmediatamente

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
