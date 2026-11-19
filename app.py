import streamlit as st
import google.generativeai as genai
import os

# 1. Configuracion de la pagina web
st.set_page_config(page_title="Chatbot Gimnasio Obregón", page_icon="GO")
st.title("Chatbot Gimnasio Obregón")
st.write("Soy el asistente virtual de tu colegio, preguntame lo que necesites sobre el colegio, horarios o normatividad.")

# 2. Conectar con la API de Google
api_key = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Por favor, configura la variable GEMINI_API_KEY en Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# 3. Leer el archivo con la información del colegio
def cargar_informacion():
    if os.path.exists("informacion.txt"):
        with open("informacion.txt", "r", encoding="utf-8") as f:
            return f.read()
    return "No hay información disponible del colegio."

contexto_colegio = cargar_informacion()

# 4. Historial del chat en pantalla
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Respuesta del bot
if user_question := st.chat_input("¿Qué información quieres saber?"):
    st.session_state.messages.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)

    instrucciones_bot = f"""
    Eres un asistente virtual amable del colegio. Responde la pregunta basandote UNICAMENTE en la siguiente informacion oficial. Si no esta la respuesta en el texto, di que no posees esa informacion.

    Informacion del colegio:
    {contexto_colegio}

    Pregunta del estudiante: {user_question}
    """

    with st.chat_message("assistant"):
        try:
            # Usamos el modelo estandar y libre de errores de v1beta
            model = genai.GenerativeModel("gemini-3.6-flash")
            response = model.generate_content(instrucciones_bot)
            respuesta_final = response.text
            
            st.markdown(respuesta_final)
            st.session_state.messages.append({"role": "assistant", "content": respuesta_final})
        except Exception as e:
            st.error(f"Error de conexión con el servidor: {e}")
