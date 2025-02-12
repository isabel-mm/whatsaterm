import streamlit as st
import pandas as pd

# ---- CSS Personalizado ----
st.markdown("""
    <style>
        /* Cambiar la fuente y hacer el diseño más limpio */
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f7f7f7;
            color: #333;
        }
        
        /* Justificar texto */
        .stMarkdown p, .stText p {
            text-align: justify;
        }

        /* Personalizar los títulos */
        .stTitle {
            color: #1f77b4;
            font-weight: bold;
        }
        
        /* Mejorar los botones */
        div.stButton > button {
            background-color: #007bff;
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 16px;
            transition: 0.3s;
        }
        
        div.stButton > button:hover {
            background-color: #0056b3;
        }
        
        /* Modificar cajas de texto */
        .stTextArea, .stTextInput {
            border-radius: 10px;
            border: 1px solid #ccc;
            padding: 8px;
        }

        /* Espaciado entre secciones */
        .block-container {
            padding-top: 30px;
        }

    </style>
""", unsafe_allow_html=True)

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
    st.title("👋 ¡Hola, bienvenid@ al experimento!")
    st.markdown(
        """
        🧑‍💻 **Objetivo del experimento**  
        En este experimento tienes que marcar los términos relacionados con la **lingüística de corpus**.

        📝 **Instrucciones:**  
        1️⃣ Introduce tu nombre en la siguiente pantalla.  
        2️⃣ Se te presentará el texto segmentado en párrafos.
        3️⃣ De manera intuitiva, anota en la columna derecha los **términos clave** que identifiques. Sepáralos con salto de línea (**enter**)
        4️⃣ Al finalizar, guarda los términos y descarga el archivo .CSV.

        💡 ¡Gracias por tu participación!
        """, unsafe_allow_html=True)

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
    st.markdown("🔎 **Lee cada párrafo y escribe los términos clave en la caja de la derecha, uno por línea (ENTER).**", unsafe_allow_html=True)

    for i, parrafo in enumerate(texto):
        key = f"terms_paragraph_{i}"
        if key not in st.session_state:
            st.session_state[key] = ""

        col1, col2 = st.columns([2, 3])  # Más espacio para la columna de términos
        with col1:
            st.markdown(f"### 📌 Párrafo {i+1}", unsafe_allow_html=True)
            st.markdown(f"<p>{parrafo}</p>", unsafe_allow_html=True)  # Justificado

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
    st.markdown(
        f"""
        🙌 **{st.session_state.user_name}, has completado la tarea.**  

        ✅ Tus términos seleccionados están listos para ser guardados.  
        📩 **Paso final:** Descarga el archivo y envíamelo a **isabel.moyano@uca.es**.
        """, unsafe_allow_html=True
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
            csv = df.to_csv(index=False, encoding="utf-8").encode("utf-8")

            st.download_button(
                label="📥 Descargar archivo CSV",
                data=csv,
                file_name="terminos_seleccionados.csv",
                mime="text/csv",
            )

    st.markdown("📩 **Cuando termines, envíame el archivo a isabel.moyano@uca.es.** ¡Gracias por participar! 😊", unsafe_allow_html=True)

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
