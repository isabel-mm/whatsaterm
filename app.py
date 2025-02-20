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
ejemplos=['Once we have identified all text varieties that should be included, we need to decide how to collect relevant specimens and which ones of these to select for inclusion. Collection is chiefly relevant from a practical point of view, and we take it up again in the following section. Text selection is a non-trivial aspect of corpus building for general corpora: since we aim at a high degree of general representativeness, we need to consider carefully the composition of our corpus. One way to go is to approximate the composition of the population as estimated in some way (cf. Brown corpus) whereas the alternative is to aim for a balance of text varieties (cf.', "The second layer of RefIND annotations is a rough classification of new referents, distinguishing, for example, <new> from <bridging> corresponding roughly to a distinction between 'brand-new' and 'evoked/implied' referents. These latter annotations are applied only to the first mentions of a referent where they are introduced into the discourse. Now let's have a look at a set of examples that illustrate the annotation practice and the rationale behind the system. Examples (7.13) -(", 'Corpus linguistics is a central approach in sociolinguistics that is interested in the use of language as dependent on a range of social factors. These are generally captured in corpus linguistics as part of the external contextual features. We have seen how essentially corpus-linguistic investigations can be levelled to address sociolinguistic questions. A major remaining challenge is the lack of sufficiently rich corpora from diverse languages that contain the relevant primary data as well as metadata.', 'The right side of the tree shows three splits for the animate referent data. Split 5 and split 9 are splits in the person data. Speech act participants (the first and second person) are significantly more likely to be expressed by a pronoun, and the first person even more so, as seen in node 10. We see that the third person referents are further', 'A final example of apparently universal patterns of spoken-language processing comes from information management and is also related to the processing of nominal expressions and their referents. But in this case, matters are more controversial, with recent research questioning a long-standing perceived view grounded in seminal work of information management by John Du', 'Note that the tables below display information about bigrams, not trigrams. That is, the tables report information about two-word co-occurrences, not three-word cooccurrences. While there will certainly be instances of a woman who in the SOAP, the table is reporting separate frequencies of a woman and woman who. You can check for yourself the frequency of a woman who in the SOAP and SCOTUS.', 'Relating composition back to corpus size, it should be clear that composition takes precedence over size: tremendously expanding the size of a corpus may not help improve its representativeness very much, as is the case with iWeb. The fact that its metadata is very sparse here adds a further downside (cf.', 'Corpus builders have to consider the use of different scripts. Since mainstream corpus linguistics focuses on English and other Western European languages, the Latinbased script used in these languages is most common, and relevant corpus software and query mechanisms are based on it. For languages with other scripts, for example, Cyrillic scripts in many languages of Eastern Europe and Central Asia or various scripts of East Asian languages (Mandarin, Japanese, etc.) corpus builders will either need to use encoding such as Unicode (cf. 5.11) or add a layer of transliteration to the corpus text. Solutions will depend on specific circumstances, and we merely point out the general requirements here.', 'There are a number of options, and we do not provide any specific suggestions here. The main point that you need to be aware of is the fact that any digital text is encoded in some form. This means you have to make sure that when working with different software or on different machines the text and letters that look the same really are the same in terms of their encoding. If encoding does not match, you will potentially not find relevant text. Moreover, you should consider differences in format: if data remain in different formats that cannot be combined for a search, then multiple searches will have to be used for corpus queries. For some purposes, such as finding an illustrative example for a paper, this may be fine. However, if you want frequency tables, n-gram counts, or proportions (cf. Chapter 5), compiling the corpus data into a standard format is an important step. If you are dealing with multiple file formats, exporting or converting everything to plain text format is probably the simplest way to compile it all together. Further options include exporting/importing texts to a single software to give the data a unified format. Also possible is compiling the corpus in multiple formats. Multi-CAST is an example where both options are available: users can work with the data in ELAN (where multiple files can be queried) or load it into R as the package multicastR (Schiborr 2018).', "The first question we can ask about the content of a corpus is how much text it contains: its size. Corpus size is typically reported as the number of wordform tokens. What size a given corpus has will depend to a major extent on the kinds of texts included and the resources required to compile these into structured collections. To get a better idea about corpus sizes, let's consider some specific examples of English language corpora, as listed in Table", 'The Brown tagset also picks up specific forms that are particularly relevant for the analysis of grammatical (sentence) structure, thus breaching strict assumptions of word class membership; this is typical of tagsets for English. For instance, different forms of the verbs be, have, and do receive their own specific tags lacking an initial V for classification as verbs, as shown in Table', "Corpora are not random bags of words. They consist more or less coherent texts, and these texts consist of ordered strings of words (cf. 2.2.1). There are multiple ways to measure the dispersion of a word or collocate. One option is a dispersion plot. This is a visualisation of where a word or collocate occurs in a corpus. Two words with the same frequency might occur often only in a handful of texts, or more consistently across the entire corpus. These words would have equal frequency, but different dispersions. Within a text, some words may be restricted to particular sections, which is also useful to know. For instance, we might see the end most often at the end of a corpus of children's stories and rarely at the beginning or in the middle of the texts in that corpus. Take a look at Gries (2010b) for more on measures of dispersion.", 'The findings from corpus-based typology also feed back into ideas about corpus building, composition, and annotation: more diverse languages require different considerations of register, representativeness, and potentially, require adaptations of annotation and querying strategies. It is still an emerging field and will help shape the more general perspective on corpus linguistics as a field in the 21st century.', "We now move away from sound to meaningful parts of words: morphemes. Let's look at two studies that use corpora to answer questions about morphology relating to the productivity of morphemes. Productive morphemes can be used with many words such as the -ness suffix for nouns deriving from adjectives in English (happiness, sadness, completeness). They can also be used to form novel words: 'she was overcome with upsetness' would probably be understandable to a reader. Non-productive morphemes can only be used with a smaller frozen subset of words, such as the -th suffix for nouns deriving from adjectives (warmth, length [from long + -th]). A novel word such as calmth would probably be confusing for most readers and older words such as dampth have fallen out of usage and have been replaced with dampness underscoring the productivity of -ness. We will look at two studies on morphological productivity:", "Some sociolinguistic variables are conditioned not by area, but by some broader social divisions. Some variants are more prestigious than others and people have different ways to show how they orient themselves to standards and norms by their use (or not) of prestige variants. But prestige is a complex notion. Sociolinguists often write about overt and covert prestige. Variants that are part of a standard or have normative valuations like being 'nicer' , 'better' , and 'correct' have overt prestige, that is, people are aware of the prestige of the variant. Some variants have covert prestige or some quality that people orient to privately or subconsciously", 'Keywords are used in some kinds of corpus linguistics to show differences between corpora or between sub-parts of a corpus. Keywords are calculated by assessing all the word frequencies in each of the two (sub)corpora and doing either chi-squared tests or log-likelihood measurements to assess what words are statistically more frequent in one (sub)corpus than in another. These are then the keywords. Usually, these kinds of keywords are lexical items (nouns, adjectives, verbs) that give us an idea of the topics in the corpus. However, the keywords could be, say, pronouns if one corpus is conversational and another is from monologic or written sources.', 'Not everyone worries about the details of statistical analyses, and when some people read through statistical analysis, they often skip over a lot of the details and just look at the p-values. Despite this, reporting only a p-value is not sufficient if you want to accurately report your results. Minimally, you need to provide the test statistic (e.g. r or χ 2 ) and the p-value if there is one, degrees of freedom if possible, as well as the amounts of tokens you looked at (n); you can enhance this by reporting some confidence intervals or error rates, so people can evaluate the test statistics themselves. When reporting multivariate analyses, it often makes sense to present data in a table, as well as in a paragraph format to guide people in interpreting the results. When stating an outcome, include the statistic in addition to stating that something is significant. Statistical abbreviations and indicators should be italicised. Here are some examples:', "Finally, requirements on corpus design notwithstanding, we should point out that CBT researchers are generally encouraged to make the most of the corpus data they have. This is particularly true for corpora drawing to a large extent on documentary corpora where limitations on data collection are highly relevant (cf. Chapter 10). For instance, stimulus-derived texts can be of much less value for a community than recordings of texts from the relevant traditional 'orature' , and documentary linguists for ethical and research-practical reasons are encouraged to comply with a community's desiderata. There may often be possibilities to bootstrap one's data in such a way that it be useful for a particular research question. Regarding, for instance, referential density research, one cannot compare uncontrolled texts across the board, as explained above. Yet, in the absence of controlled texts, one can still aim at finding overall comparable contexts to", 'The actual distribution of such forms across texts of different modes is beyond the discussion in this chapter and is more a matter of systematic register studies, such as those mentioned in 3.1.6. What is relevant for our purposes here is that corpus and tagset developers entertain a considerable degree of freedom in designing tagsets to serve their specific needs, so that tags do not necessarily reflect the absolute exactness of linguistic analysis and classification. In other words, the maxim for the development of tagsets -and annotation systems more generally -is not that they are linguistically 100% accurate but that they are useful and overall consistent in their operationalisation.', "Corpus linguists are interested in how linguistic data is conditioned by context. To achieve this, we need annotations and metadata to turn collections of data into corpora that will form the basis for corpus-linguistic investigations of language use, and what this tells us about the structure of a specific language's grammar, lexicon, etc., as well as the conventions of the language use and that of the community members' thereof.", 'In Section 7.2 we present a selection of conventions for annotation that target different linguistic levels. We will refer to additional literature in the further reading section for more exhaustive overviews. Our main purpose here is to explain the basic implementation of corpus annotations and how they add value to a corpus by enhancing its amenability to a wider range of research questions. We will repeatedly refer back to Chapters 4 and 5 where different types of annotation were relevant. Section 7.3 is devoted to comparative corpus annotations in the context of corpus-based typology. This section is tightly connected with Chapter 11 where we will explain various types of research that builds on these or similar types of annotation systems.', "The captivating aspect of UD annotations is that they are relatively easy to implement but enable a huge range of investigations. For instance, you can easily determine the expression of subjects and objects by pronouns and NPs (cf. our investigation of Vera'a). You can also determine the relative length and complexity of phrases (understood as dependency structures) by considering the number of head indices in the head column cross-referencing the head word of the phrase in question, or all phrases dependent on the verb node. These findings can then be related to the function of these phrases -or their dependency relation to the verb -comparing, for example, subject and object NPs. Similarly, phrase length can be related to their linear position within the clause by relating these to the ID numbers of their constituents; in this way NP complexity can be related to their ordering in the clause, a prominent research question in typology (see Chapter 11). Finally, constituent order in terms of grammatical relations can be determined in relation to the word form IDs. These questions link to a range of well-established research agendas on constituent order and languages processing, and we will outline some UD-based research in this area in Chapter 11 on typology.", 'The first half of this textbook focuses on the basics of corpus linguistics (Chapter 2) and types of corpora, including what is relevant for assessing the make-up of a corpus (Chapter 3). We give examples of corpus linguistic research in Chapter 4, showing that the corpus linguistic approach is possible for many levels of linguistic analysis and diverse languages. The second part of the book focuses on some of the tasks you might do in conducting your own corpus study including querying a corpus and evaluating the results (Chapter 5), and composing and building your own corpus (Chapter 6). In this vein, we also introduce various corpus annotation schemata which give various kinds of information that cannot be read from the corpus text itself (', 'Boxplots are a common graphical way of depicting the spread of the data and use the IQR. The data that falls within the IQR will be in the box in the centre of the plot. The horizontal line across the box indicates the median. The so-called whiskers (made up of the dotted vertical lines and solid horizontal lines that go out from the box) mark the 1.5 IQR above the third quartile and below the first quartile. In a normal distribution, the whiskers will be of the same length; if they have different lengths then it is a sign that the distribution is skewed.', "Half of the London-Lund Corpus (LLC) (LLC; Svartvik 1990) consists of spoken texts, and for this a tagset was designed specifically to capture some features of words in spoken texts. 3 The LLC tagset is much larger than the Brown tagset, comprising 204 tags, reflecting finer-grained and additional grammatical distinctions, for example, the case forms of pronouns, and including cliticised forms whereby clitic and host are treated as one 'contracted' token word (cf 2.2.2). Tagging of contracted forms combines the two underlying word forms with a <*>, resulting in tags like <BHdem*VB+3>, where the latter part <VB+3> stands for '3rd person form of the verb be' thus differentiating that's from that. In addition to tags for these, the LLC tagset contains tags for expression -including multi-word expressions -that the authors consider characteristic of spoken language, as listed in Table", 'How can metalinguistic knowledge be recorded during language documentation and how are they relevant to corpus building? First of all, it may come up in naturally occurring, recorded conversations: in many communities, people talk about the use of certain forms, in particular if they feel that one or the other variant is of lower prestige, like the lack of subject agreement in some English varieties. Second, capturing metalinguistic knowledge can also take the form of recording discussions of linguistic structures between the researcher and one or more users of a given language. Third, writing in a native language may provide valuable clues as to metalinguistic knowledge, for instance, with regard to how a stream of speech is broken down into segments like words (see', "Another type of data linked to corpus data and raw data is metadata. Metadata is literally 'data about data' . In corpora, it encompasses properties of all data types, as well as data about the corpus as a whole and its creation process. Metadata capture properties of the (written) corpus text (text format, encoding, script, structure of annotations, etc.), properties of the original text, that is, the raw data linked to corpus data (audio and video formats, recording equipment, publication details, etc.), and aspects of the relationship between primary data and raw data (how do corpus text files and original publication files, in particular, video and audio files, link to each other? Is there time-alignment, and how is it encoded? etc.). In addition to these, metadata is also collected about the situational features of texts (cf. 2.2.4).", 'The central premise of corpus linguistics is that all of the language-internal andexternal contextual features are relevant to the way that people use language. In other words, the use of linguistic forms is always subject to certain conditions. In corpus linguistics, we are essentially interested in how various structures (sounds, words, constructions) are used in particular contexts characterised by internal and external features; how possible variation in usage and choices between alternative structures (the so-called variants of a variable) can be correlated with such features, and how the use of particular forms can then be explained in terms of specific (qualitative) mechanisms relating to such features (see 4.', '(5) analyse frequencies and distributions of your data While it would be ideal if we could give readers one straightforward, foolproof way of doing this, we cannot. Corpus data comes in many different formats, and there are easily hundreds of methods, tools, and strategies that are possible. What we might recommend today (a certain corpus tool, a certain programming package, or module) might not be available three years from now, or might have advanced so much that our information is out-of-date. This is both the exciting and frustrating part of corpus linguistics. There is always something new being developed that can improve our work, but it means specific previous strategies eventually become obsolete. This chapter will guide you through common strategies for searching and analysing data.', "To obtain frequencies or examples, one must engage with the corpus or 'query' it. Most corpus linguists will not read through an entire corpus. Usually, it is too large for us to engage with systematically. Instead, we will pull out relevant information and put it into a format that makes it possible to study it further. Some kind of software on a computer or interface on the web will be used to do this. Most text editors and word processing programs have a search function that will allow a user to find segments, words, or phrases. Specialised corpus software and web interfaces also have means of finding examples and often have ways to save those examples to a new document or spreadsheet for further analysis. Many of these programs will provide basic descriptive statistics of the data, such as number of occurrences, bigram frequency (cf. 5.6), mutual information (MI) (cf. 5.7), etc. It is worthwhile to explore various tools whether you are new to corpus linguistics or are a seasoned veteran."]

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
