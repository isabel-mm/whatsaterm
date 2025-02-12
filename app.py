import streamlit as st
import pandas as pd

# ---- Configuración del estado de sesión ----
if "app_stage" not in st.session_state:
    st.session_state.app_stage = "inicio"

if "selected_terms" not in st.session_state:
    st.session_state.selected_terms = {}

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

# ---- Texto de ejemplo segmentado ----
texto = [
    "La lingüística de corpus es una metodología que emplea corpus electrónicos para analizar fenómenos lingüísticos con base en datos reales.",
    "Se distingue por el uso de herramientas computacionales para identificar patrones y frecuencias léxicas.",
    "Los corpus permiten realizar estudios empíricos en lingüística aplicada, traducción, lexicografía y otros campos.",
    "A través del análisis de corpus se pueden identificar tendencias en el lenguaje, neologismos y usos específicos en diferentes registros."
]

# ---- Pantalla 1: Introducción ----
if st.session_state.app_stage == "inicio":
    st.title("👋 ¡Bienvenid@ al experimento!")
    st.write(
        """
        🧑‍💻 **Objetivo del experimento**  
        Queremos estudiar cómo identificas términos clave en textos de lingüística de corpus.

        📝 **Instrucciones:**  
        1️⃣ Introduce tu nombre en la siguiente pantalla.  
        2️⃣ Lee cada párrafo del texto (columna izquierda).  
        3️⃣ Escribe los **términos clave** que identifiques en la **columna derecha**, **uno por línea (ENTER)**.  
        4️⃣ Al finalizar, guarda y envía tus resultados.

        💡 ¡Gracias por tu participación!
        """
    )

    if st.button("🚀 Comenzar"):
        st.session_state.app_stage = "nombre"
        st.rerun()

# ---- Pantalla 2: Introducir Nombre ----
elif st.session_state.app_stage == "nombre":
    st.title("✍ Introduce tu nombre")
    user_input_name = st.text_input("Nombre:", value=st.session_state.user_name)

    if user_input_name:
        st.session_state.user_name = user_input_name  # Guardamos el nombre en session_state

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅ Volver"):
            st.session_state.app_stage = "inicio"
            st.rerun()

    with col2:
        if st.session_state.user_name and st.button("➡ Continuar"):
            st.session_state.app_stage = "seleccion"
            st.rerun()

# ---- Pantalla 3: Selección de términos por párrafo ----
elif st.session_state.app_stage == "seleccion":
    st.title("📝 Selección de términos")
    st.write("🔎 **Lee cada párrafo y escribe los términos clave en la caja de la derecha, uno por línea (ENTER).**")

    for i, parrafo in enumerate(texto):
        key = f"terms_paragraph_{i}"
        if key not in st.session_state:
            st.session_state[key] = ""

        col1, col2 = st.columns([2, 3])  # Más espacio para la columna de términos
        with col1:
            st.markdown(f"### 📌 Párrafo {i+1}")
            st.write(parrafo)
        
        with col2:
            # Ahora usamos text_area sin modificar `st.session_state` directamente
            st.text_area("Términos (sepáralos con ENTER)", key=key, height=100)

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅ Volver"):
            st.session_state.app_stage = "nombre"
            st.rerun()

    with col2:
        if st.button("✅ Finalizar tarea"):
            # Guardamos los términos en selected_terms ANTES de cambiar de pantalla
            st.session_state.selected_terms = {
                f"Párrafo {i+1}": st.session_state[f"terms_paragraph_{i}"]
                for i in range(len(texto)) if st.session_state[f"terms_paragraph_{i}"]
            }
            st.session_state.app_stage = "guardar"
            st.rerun()

# ---- Pantalla 4: Guardar tarea y despedida ----
elif st.session_state.app_stage == "guardar":
    st.title("🎉 ¡Gracias por participar!")
    st.write(
        f"""
        🙌 **{st.session_state.user_name}, has completado la tarea.**  

        ✅ Tus términos seleccionados están listos para ser guardados.  
        📩 **Paso final:** Descarga el archivo y envíamelo a **isabel.moyano@uca.es**.
        """
    )

    # ---- Formatear términos correctamente antes de exportar ----
    formatted_terms = [
        {"Párrafo": key, "Términos": "; ".join(value.split("\n")), "Usuario": st.session_state.user_name}
        for key, value in st.session_state.selected_terms.items()
    ]

    # ---- Exportar términos a CSV en utf-8 ----
    if st.button("📥 Descargar términos seleccionados"):
        if not formatted_terms:
            st.error("⚠ No hay términos seleccionados.")
        else:
            df = pd.DataFrame(formatted_terms)
            csv = df.to_csv(index=False, encoding="utf-8").encode("utf-8")  # Manteniendo utf-8

            st.download_button(
                label="📥 Descargar archivo CSV",
                data=csv,
                file_name="terminos_seleccionados.csv",
                mime="text/csv",
            )

    st.write("📩 **Cuando termines, envíame el archivo a isabel.moyano@uca.es.** ¡Gracias por participar! 😊")

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅ Volver"):
            st.session_state.app_stage = "seleccion"
            st.rerun()
    
    with col2:
        if st.button("🔄 Reiniciar experimento"):
            st.session_state.app_stage = "inicio"
            st.session_state.selected_terms = {}
            st.session_state.user_name = ""
            st.rerun()
