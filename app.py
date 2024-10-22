import streamlit as st
import os
import json
import pandas as pd

st.set_page_config(
    page_title="Ley Marco de Ciberseguridad y Protección de Datos Personales",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Directorios de las carpetas
directories = {
    "articulos": "data/articles/",
    "resumen": "data/summary/",
    "preguntas": "data/questions/"
}

# Leer el archivo CSV y crear un diccionario para mapear los códigos de leyes a sus nombres
laws_df = pd.read_csv('data/laws.csv', delimiter=';')
laws_dict = dict(zip(laws_df['ley'].astype(str), laws_df['nombre']))

# Función para leer archivos JSON de una carpeta y generar un diccionario
def load_json_files(directory):
    json_dict = {}
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                # Carga el contenido del archivo JSON
                json_data = json.load(f)
                # Extrae el nombre del archivo sin extensión para usarlo como clave
                key = filename.replace('.json', '')
                json_dict[key] = json_data
    return json_dict

# Crear los diccionarios para cada tipo
dct_articulos = load_json_files(directories["articulos"])
dct_resumen = load_json_files(directories["resumen"])
dct_preguntas = load_json_files(directories["preguntas"])


# Renombrar diccionarios
dct_articulos = {laws_dict[key]: value for key, value in dct_articulos.items() if key in laws_dict}
dct_resumen = {laws_dict[key]: value for key, value in dct_resumen.items() if key in laws_dict}
dct_preguntas = {laws_dict[key]: value for key, value in dct_preguntas.items() if key in laws_dict}




# Función para mostrar una pregunta y validar la respuesta
def mostrar_pregunta(pregunta, opciones, respuesta_correcta, key):
    st.write(pregunta)
    seleccion = st.radio("Selecciona una opción:", opciones, key=key)  # Asignar key única
    if st.button("Verificar respuesta", key=f"boton_{key}"):
        if seleccion == respuesta_correcta:
            st.success("¡Correcto!")
        else:
            st.error("Incorrecto. La respuesta correcta es: " + respuesta_correcta)



def main():
    """
    Main function to set up the Streamlit app layout.
    """
    cs_sidebar()
    cs_body()
    return None

# Funciones
def cs_sidebar():
    """
    Sidebar con un resumen de la Ley Marco de Ciberseguridad y Protección de Datos Personales.
    """
    st.sidebar.title("Ley Marco de Ciberseguridad y Protección de Datos Personales")

    # Mostrar logo
    logo_url = "images/hammer.png"
    st.sidebar.image(logo_url, width=200)

    # Objetivos de la Ley
    with st.sidebar:
        with st.expander("🎯 Objetivos"):
            st.markdown(
                """
                1. **Principios Clave**: Familiarizarse con ciberseguridad y protección de datos.
                2. **Derechos y Responsabilidades**: Conocer los derechos de los titulares y las obligaciones de las organizaciones.
                3. **Conciencia en Seguridad**: Promover prácticas para proteger la información.
                4. **Cumplimiento Normativo**: Proveer herramientas para cumplir con la legislación.
                5. **Educación Continua**: Ofrecer recursos para el aprendizaje en ciberseguridad.
                """
            )

        # Información relevante
        with st.expander("🌐 Información Relevante"):
            st.markdown(
                """
                1. **Ámbito**: Aplicable a organismos públicos y privados en Chile.
                2. **Derechos de los Titulares**: Derecho a acceder, rectificar y oponerse al tratamiento de datos.
                3. **Obligaciones**: Proteger la integridad y confidencialidad de los datos.
                4. **Sanciones**: Infracciones pueden resultar en sanciones económicas y legales.

                Más información:  
                - [Ley 21.663 - Ley Marco de Ciberseguridad](https://www.bcn.cl/leychile/navegar?idNorma=1202434)
                - [Ley 19.628 - Ley Sobre Protección de la Vida Privada](https://www.bcn.cl/leychile/navegar?idNorma=141599)

                > **Nota**: Se Agrega la Ley de Protección de Datos Personales (Transitoria).
                """
            )







def cs_body():
    """
    Create content sections for the main body of the Streamlit cheat sheet with Python examples.
    """
    st.title("🏛️ Ley Marco de Ciberseguridad y Protección de Datos Personales")  # Título de la sección

    # Agregar selectbox en el sidebar
    ley_seleccionada = st.sidebar.selectbox("✏️ Selecciona una ley:", list(dct_articulos.keys()))

    # Tab menu
    tab1, tab2, tab3 = st.tabs(
        ["⚖️ Artículos", "📝 Resumen", "🎲 Ejercicios"]
    )

    with tab1:
        st.header("Detalles de las Leyes")
        st.subheader(ley_seleccionada)
        # Mostrar los artículos en un expander
        for titulo, articulos in dct_articulos[ley_seleccionada].items():
            with st.expander(titulo):  # Usar expander para cada título
                # Checkboxes para cada artículo dentro del título
                for articulo, contenido in articulos.items():
                    mostrar_articulo = st.checkbox(articulo, key=articulo)
                    if mostrar_articulo:
                        st.write(contenido)

    with tab2:
        st.header("Resumen de las Leyes")
        st.subheader(ley_seleccionada)
        # Iterar sobre el diccionario y mostrar los títulos y descripciones
        for titulo, contenido in dct_resumen[ley_seleccionada].items():
            with st.expander(titulo):  # Usar expander para cada título
                st.markdown("📋 **Artículos**:")
                st.write(", ".join(contenido["articulos"]))  # Mostrar los artículos
                st.markdown("✏️ **Descripción**:")
                st.write(contenido["descripcion"])  # Mostrar la descripción del título

    with tab3:
        # Título del aplicativo
        st.header("Aplicativo de Preguntas y Respuestas")
        st.subheader(ley_seleccionada)
        # Iterar sobre el diccionario y mostrar las preguntas por título
        for titulo, preguntas in dct_preguntas[ley_seleccionada].items():
            with st.expander(titulo):  # Usar expander para cada título
                for idx, pregunta_info in enumerate(preguntas):
                    pregunta = pregunta_info["pregunta"]
                    opciones = pregunta_info["opciones"]
                    respuesta_correcta = pregunta_info["respuesta_correcta"]
                    mostrar_pregunta(pregunta, opciones, respuesta_correcta, key=f"{titulo}_{idx}")

    css = '''
    <style>
        /* Ajusta el tamaño del texto en las pestañas (Tabs) */
        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
            font-size: 1.5rem; /* Tamaño del texto en las pestañas */
        }

        /* Opción adicional: Ajusta el tamaño de los encabezados dentro de los expanders */
        .st-expander h1, .st-expander h2, .st-expander h3 {
            font-size: 4rem; /* Tamaño de los encabezados dentro de los expanders */
        }

        /* Ajustar el tamaño del texto del selectbox en el sidebar */
        .sidebar .stSelectbox label {
            font-size: 1.5rem; /* Ajusta este valor para cambiar el tamaño del texto */
        }

    </style>
    '''

    st.markdown(css, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
