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
    "Corpus linguistics started as an enterprise interested in words, their frequency, and their contexts. Even if a corpus is basic, simply a string of wordforms with no other annotation, it is easy to search for individual words since usually words are a kind of string of characters, separated by white space. There are many corpus studies that compare lexemes, especially near-synonyms and purported synonyms. Corpus searches of words that have similar meanings can show that synonyms can occur in quite different contexts. The differing contexts, then, should be taken into account as part of the definitions of words.",
    "As discussed in 3.1.1, corpus size is important because we know that in a large sample, we have a better chance of finding what we are looking for, and a better chance of seeing typical patterns of usage. A small sample is more likely to be affected by chance and we may see spurious results. Small samples, unless carefully balanced, will be much more affected by the genre of the source content.",
    "The multiple annotation schemes of SCOPIC are organised along functional categories. Each language in the study is annotated for expressions that relate to many functional categories relevant to social cognition. Within each broad functional category, researchers code a \"TAG\" and a \"TERM\" for each instance of the phenomenon. A TAG comes from a closed and cross-linguistically fixed list of category choices and indicates the type of expression being used for the relevant instantiation of a particular functional category.",
    "Correspondence Analysis and Multiple Correspondence Analysis: used for categorical, non-numeric dependent variables, plots dependent variables, as well as independent variables associations measured as chi-square distances.",
    "Parallel text corpora: texts that are translational equivalents, for example, translations of The Bible text, like the Gospel of Mark.",
    "Statistical description and analysis. These quantify structural tokens in usage, where statistical universal in traditional typology quantify structural types as part of individual language systems. Classification of a language as \"pro-drop\" in relevant frameworks involves more intricate diagnostics than how frequent zeroes are in discourse.",
    "Searching for such phenomena requires some string information and some annotation. However, linguists also use corpora to look for phenomena at the constituent level in syntax. This can be difficult because string information is less useful at this level to identify tokens. Take for instance a category like subject or object. These could be any number of different nouns, NPs, or even zeros.",
    "A famous example of a treebank with constituent structure annotation is the Penn Treebank developed at the University of Pennsylvania, first released in 1992 comprising texts with 2.8 million token words.",
    "Corpus-based methods have been increasingly employed in contrastive linguistics. The comparison of linguistic structures across languages has benefited from large, systematically compiled corpora.",
    "Annotation schemes vary depending on the research goals. While some schemes prioritize morphological information, others focus on syntactic structures.",
    "Measures of dispersion provide insights into the stability of word frequency across different text types.",
    "Synchronic and diachronic corpus studies provide different perspectives on linguistic change.",
    "Frequency lists generated from large corpora reveal significant patterns in language usage.",
    "Relative frequency measures are more informative than absolute counts in corpus comparisons.",
    "Tagging systems in corpus linguistics have evolved to accommodate multi-layered annotation schemes.",
    "Collocation analysis plays a vital role in corpus linguistics. Identifying frequent co-occurrences of words provides insights into phraseology and lexical patterns.",
    "Data structures in corpus research must be efficiently organized to allow for rapid querying and statistical analysis.",
    "Logistic regression is frequently used in corpus linguistics to model categorical linguistic outcomes.",
    "Data annotation is a crucial step in corpus construction, ensuring accuracy in linguistic analyses.",
    "Text files containing linguistic data must be structured to allow compatibility with analysis tools.",
    "Natural language processing techniques are widely used in corpus-based studies to extract relevant linguistic patterns.",
    "Statistical significance tests help determine whether observed patterns in corpus data are due to chance.",
    "Corpus-driven approaches focus on deriving linguistic theories from actual language use rather than pre-established models.",
    "General corpus studies aim to cover a broad range of linguistic phenomena to ensure applicability across different research questions.",
    "The independence of observations is a key assumption in statistical models applied to corpus data.",
    "Word frequency lists provide insights into core vocabulary and the distribution of lexical items.",
    "The representation of different text types in a corpus affects the generalizability of linguistic findings.",
    "Corpus construction requires careful planning to ensure balance and representativeness of the data.",
    "Parts-of-speech tagging is an essential preprocessing step in corpus linguistics, facilitating syntactic analysis.",
    "Measures of dispersion indicate how evenly a word is distributed across different sections of a corpus.",
    "The structure of corpus files must allow for efficient indexing and retrieval of linguistic information."
]

# ---- Pantalla 1: Introducción ----
if st.session_state.app_stage == "inicio":
    st.title("👋 ¡Hola, bienvenid@ al experimento!")
    
    st.markdown(
        "🧑‍💻 **Objetivo del experimento**  \n"
        "En este experimento tienes que marcar los términos relacionados con la **lingüística de corpus**.  \n\n"
        "📝 **Instrucciones:**  \n\n"
        "1️⃣ **Introduce tu nombre en la siguiente pantalla.**  \n\n"
        "2️⃣ **Se te presentará el texto segmentado en párrafos.**  \n\n"
        "3️⃣ **De manera intuitiva, anota en la columna derecha los términos clave que identifiques.**  \n"
        "   💡 **Sepáralos con salto de línea (ENTER).**  \n\n"
        "4️⃣ **Al finalizar, guarda los términos y descarga el archivo `.CSV`.**  \n\n"
        "💡 ¡Gracias por tu participación!", 
        unsafe_allow_html=True
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
    st.markdown("🔎 **Lee cada párrafo y escribe los términos clave en la caja de la derecha, uno por línea (ENTER).**", unsafe_allow_html=True)

    for i, parrafo in enumerate(texto):
        key = f"terms_paragraph_{i}"
        if key not in st.session_state:
            st.session_state[key] = ""

        col1, col2 = st.columns([2, 3])  # Más espacio para la columna de términos
        with col1:
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
