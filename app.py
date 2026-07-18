import streamlit as st
import google.generativeai as genai
import os

 

# 1. Configuración de la página web
st.set_page_config(page_title="Chatbot Escolar", page_icon="🤖")
st.title("🤖 Chatbot Oficial del Colegio")
st.write("Pregúntame lo que necesites sobre el colegio, horarios o normatividad.")

 

# 2. Conectar con la Inteligencia Artificial de Google
# Intentará leer la clave desde los secretos de la nube o desde las variables de tu PC
api_key = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

 

if not api_key:
    st.error("Por favor, configura la variable de entorno GEMINI_API_KEY.")
    st.stop()

 

genai.configure(api_key=api_key)

 

# 3. Leer el archivo de texto con la información del colegio
def cargar_informacion():
    if os.path.exists("informacion.txt"):
        with open("informacion.txt", "r", encoding="utf-8") as f:
            return f.read()
    return "No hay información disponible del colegio."

 

contexto_colegio = cargar_informacion()

 

# 4. Historial del chat en la pantalla
if "messages" not in st.session_state:
    st.session_state.messages = []

 

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

 

# 5. Lógica cuando el usuario hace una pregunta
if user_question := st.chat_input("¿A qué hora inicia el descanso?"):
    # Mostrar la pregunta del usuario
    st.session_state.messages.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)

 

    # Crear las instrucciones para el bot combinando tu documento con la pregunta
    instrucciones_bot = f"""
    Eres un asistente virtual amable del colegio. Responde las preguntas de los estudiantes basándote ÚNICAMENTE en la siguiente información oficial. Si la respuesta no está en el texto, di amablemente que no posees esa información.

   

    Información oficial:
    {contexto_colegio}

   

    Pregunta del estudiante: {user_question}
    """

 

    # Llamar al modelo de Google para obtener la respuesta
    with st.chat_message("assistant"):
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(instrucciones_bot)
            respuesta_final = response.text
            st.markdown(respuesta_final)
            st.session_state.messages.append({"role": "assistant", "content": respuesta_final})
        except Exception as e:
            st.error("Hubo un error al conectar con el servidor de IA.")