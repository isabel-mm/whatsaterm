import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# ---- Configuración inicial ----
st.title("Selección de términos en lingüística de corpus")
st.write("Selecciona términos con el ratón y haz clic en 'Marcar término' para guardarlos.")

# Entrada del nombre del usuario
user_name = st.text_input("Nombre:")

# ---- Texto de ejemplo ----
texto = """La lingüística de corpus es una metodología que emplea corpus electrónicos para analizar fenómenos lingüísticos con base en datos reales. Se distingue por el uso de herramientas computacionales para identificar patrones y frecuencias léxicas."""

# ---- Estado de sesión para almacenar términos seleccionados ----
if "selected_terms" not in st.session_state:
    st.session_state.selected_terms = []

if "current_selection" not in st.session_state:
    st.session_state.current_selection = ""

# ---- Mostrar el texto en pantalla ----
st.write("### Texto:")
st.markdown(
    f"""
    <div id='text-block' style='border:1px solid gray; padding:10px;'>
        {texto}
    </div>
    """,
    unsafe_allow_html=True,
)

# ---- JavaScript para capturar la selección de texto ----
custom_js = """
<script>
    document.addEventListener("mouseup", function() {
        var selectedText = window.getSelection().toString().trim();
        if (selectedText.length > 0) {
            var streamlitInput = window.parent.document.getElementById("selected-text-input");
            if (streamlitInput) {
                streamlitInput.value = selectedText;
                streamlitInput.dispatchEvent(new Event('input', { bubbles: true }));
            }
        }
    });
</script>
"""

components.html(custom_js, height=0)

# ---- Campo oculto para almacenar el texto seleccionado ----
selected_text = st.text_input("Texto seleccionado automáticamente:", key="selected-text-input")

# ---- Actualizar la selección en el estado de sesión ----
if selected_text:
    st.session_state.current_selection = selected_text

# ---- Mostrar el término seleccionado antes de guardarlo ----
st.write(f"**Texto seleccionado:** {st.session_state.current_selection if st.session_state.current_selection else '(Selecciona un término)'}")

# ---- Botón para marcar el término seleccionado ----
if st.button("Marcar término"):
    if st.session_state.current_selection and st.session_state.current_selection not in st.session_state.selected_terms:
        st.session_state.selected_terms.append(st.session_state.current_selection)
        st.success(f"Término '{st.session_state.current_selection}' guardado.")
        st.session_state.current_selection = ""  # Resetear la selección

# ---- Mostrar términos seleccionados ----
st.write("### Términos seleccionados:")
if st.session_state.selected_terms:
    for term in st.session_state.selected_terms:
        st.write(f"- {term}")
else:
    st.warning("No hay términos seleccionados.")

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
