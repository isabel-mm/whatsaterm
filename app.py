import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# ---- Manejo del estado de la pantalla ----
if "app_stage" not in st.session_state:
    st.session_state.app_stage = "inicio"  # Primera pantalla

# ---- Pantalla de Bienvenida ----
if st.session_state.app_stage == "inicio":
    st.title("Bienvenida a la herramienta de selección de términos")
    st.write(
        """
        Esta aplicación te permitirá seleccionar términos de un texto y exportarlos en un archivo CSV.
        
        **Instrucciones**:
        1. Lee el texto que se te presentará.
        2. Selecciona con el ratón los términos relevantes.
        3. Haz clic en "Marcar término" para guardarlo.
        4. Una vez seleccionados todos los términos, puedes exportarlos.

        ¡Cuando estés listo, haz clic en "Comenzar"! 😊
        """
    )

    if st.button("Comenzar"):
        st.session_state.app_stage = "seleccion"
        st.rerun()

# ---- Pantalla de Selección de Términos ----
elif st.session_state.app_stage == "seleccion":
    st.title("Selección de términos en lingüística de corpus")
    st.write("Selecciona términos con el ratón y haz clic en 'Marcar término' para guardarlos.")

    # ---- Entrada del nombre del usuario ----
    user_name = st.text_input("Nombre:")

    # ---- Texto de ejemplo ----
    texto = """La lingüística de corpus es una metodología que emplea corpus electrónicos para analizar fenómenos lingüísticos con base en datos reales. Se distingue por el uso de herramientas computacionales para identificar patrones y frecuencias léxicas."""

    # ---- Estado de sesión para almacenar términos seleccionados ----
    if "selected_terms" not in st.session_state:
        st.session_state.selected_terms = []

    if "current_selection" not in st.session_state:
        st.session_state.current_selection = ""

    # ---- JavaScript para capturar la selección de texto ----
    selection_js = """
    <script>
        function captureSelection() {
            var selectedText = window.getSelection().toString().trim();
            if (selectedText.length > 0) {
                const streamlitInput = window.parent.document.querySelector('textarea[data-testid="stTextArea"]');
                if (streamlitInput) {
                    streamlitInput.value = selectedText;
                    streamlitInput.dispatchEvent(new Event('input', { bubbles: true }));
                }
            }
        }
        document.addEventListener("mouseup", captureSelection);
    </script>
    """

    # ---- Mostrar el texto en pantalla ----
    st.markdown(
        f"""
        <div id='text-block' style='border:1px solid gray; padding:10px; cursor:text;'>{texto}</div>
        """,
        unsafe_allow_html=True,
    )

    components.html(selection_js, height=0)

    # ---- Captura la selección en un campo oculto ----
    selected_text = st.text_area("Texto seleccionado automáticamente:", key="selected-text-input")

    # ---- Mostrar el término seleccionado ----
    st.write(f"**Texto seleccionado:** {selected_text if selected_text else '(Selecciona un término)'}")

    # ---- Botón para marcar el término seleccionado ----
    if st.button("Marcar término"):
        if selected_text and selected_text not in st.session_state.selected_terms:
            st.session_state.selected_terms.append(selected_text)
            st.success(f"Término '{selected_text}' guardado.")

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

    # ---- Botón para regresar a la pantalla de inicio ----
    if st.button("Volver a la pantalla de inicio"):
        st.session_state.app_stage = "inicio"
        st.rerun()
