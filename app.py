import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# ---- Manejo del estado de la pantalla ----
if "app_stage" not in st.session_state:
    st.session_state.app_stage = "inicio"  # Primera pantalla

if "selected_terms" not in st.session_state:
    st.session_state.selected_terms = []

if "current_selection" not in st.session_state:
    st.session_state.current_selection = ""

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

# ---- Pantalla 1: Introducción ----
if st.session_state.app_stage == "inicio":
    st.title("Bienvenida al experimento")
    st.write(
        """
        En este experimento, queremos estudiar la selección de términos en textos de lingüística de corpus.
        
        **Instrucciones**:
        1. Introduce tu nombre en la siguiente pantalla.
        2. Lee el texto presentado.
        3. Selecciona los términos clave con el ratón y márcalos.
        4. Cuando termines, guarda tus resultados y envíalos.

        ¡Haz clic en "Siguiente" para continuar!
        """
    )

    if st.button("Siguiente"):
        st.session_state.app_stage = "nombre"
        st.rerun()

# ---- Pantalla 2: Introducir Nombre ----
elif st.session_state.app_stage == "nombre":
    st.title("Introduce tu nombre")
    st.session_state.user_name = st.text_input("Nombre:")

    if st.session_state.user_name:
        if st.button("Siguiente"):
            st.session_state.app_stage = "seleccion"
            st.rerun()

# ---- Pantalla 3: Selección de términos ----
elif st.session_state.app_stage == "seleccion":
    st.title("Selección de términos")
    st.write("Selecciona términos con el ratón y haz clic en 'Marcar término' para guardarlos.")

    # ---- Texto de ejemplo ----
    texto = """La lingüística de corpus es una metodología que emplea corpus electrónicos para analizar fenómenos lingüísticos con base en datos reales. Se distingue por el uso de herramientas computacionales para identificar patrones y frecuencias léxicas."""

    # ---- JavaScript para capturar la selección de texto ----
    selection_js = """
    <script>
        function captureSelection() {
            var selectedText = window.getSelection().toString().trim();
            if (selectedText.length > 0) {
                const inputField = window.parent.document.querySelector('textarea[data-testid="stTextArea"]');
                if (inputField) {
                    inputField.value = selectedText;
                    inputField.dispatchEvent(new Event('input', { bubbles: true }));
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
            st.session_state.current_selection = ""  # Resetear selección
            st.experimental_rerun()

    # ---- Mostrar términos seleccionados ----
    st.write("### Términos seleccionados:")
    if st.session_state.selected_terms:
        for term in st.session_state.selected_terms:
            st.write(f"- {term}")
    else:
        st.warning("No hay términos seleccionados.")

    # ---- Botón para finalizar la selección ----
    if st.button("Finalizar tarea"):
        st.session_state.app_stage = "guardar"
        st.rerun()

# ---- Pantalla 4: Guardar tarea y despedida ----
elif st.session_state.app_stage == "guardar":
    st.title("Finalización del experimento")
    st.write(
        f"""
        ¡Gracias por participar, {st.session_state.user_name}! 😊  
        
        Tus términos seleccionados están listos para ser guardados.  

        **Paso final**: Descarga el archivo y envíamelo a **isabel.moyano@uca.es**.
        """
    )

    # ---- Notas del usuario ----
    user_notes = st.text_area("Notas u observaciones:")

    # ---- Exportar términos a CSV ----
    if st.button("Descargar términos seleccionados"):
        if not st.session_state.selected_terms:
            st.error("⚠ No hay términos seleccionados.")
        else:
            data = {
                "Término": st.session_state.selected_terms,
                "Usuario": [st.session_state.user_name] * len(st.session_state.selected_terms),
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

    st.write("Cuando termines, envíame el archivo a isabel.moyano@uca.es. ¡Gracias por participar! 😊")

    # ---- Botón para reiniciar la tarea ----
    if st.button("Volver a la pantalla de inicio"):
        st.session_state.app_stage = "inicio"
        st.session_state.selected_terms = []
        st.session_state.user_name = ""
        st.rerun()
