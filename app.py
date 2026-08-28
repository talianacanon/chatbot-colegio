import streamlit as st
from google import genai
import os

# 1. Configuraci贸n de la p谩gina web
st.set_page_config(page_title="Chatbot Escolar", page_icon="馃")
st.title("馃 Chatbot Oficial del Colegio")
st.write("Preg煤ntame lo que necesites sobre el colegio, horarios o normatividad.")

# 2. Conectar con la Inteligencia Artificial de Google (Gemini)
api_key = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Por favor, configura la variable de entorno GEMINI_API_KEY en Secrets.")
    st.stop()

# Crear cliente oficial de Google GenAI
client = genai.Client(api_key=api_key)

# 3. Leer el archivo de texto con la informaci贸n del colegio
def cargar_informacion():
    if os.path.exists("informacion.txt"):
        with open("informacion.txt", "r", encoding="utf-8") as f:
            return f.read()
    return "No hay informaci贸n disponible del colegio."

contexto_colegio = cargar_informacion()

# 4. Historial del chat en pantalla
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. L贸gica de interacci贸n y consulta
if user_question := st.chat_input("驴A qu茅 hora inicia el descanso?"):
    # Mostrar la pregunta del usuario
    st.session_state.messages.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)

    # Definir las instrucciones y contexto para el modelo
    instrucciones_bot = f"""
    Eres un asistente virtual amable del colegio. Responde las preguntas de los estudiantes bas谩ndote 脷NICAMENTE en la siguiente informaci贸n oficial. Si la respuesta no est谩 en el texto, di amablemente que no posees esa informaci贸n.
    
    Informaci贸n oficial del colegio:
    {contexto_colegio}
    
    Pregunta del estudiante: {user_question}
    """

    # Enviar consulta al servidor de Google
    with st.chat_message("assistant"):
        try:
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=instrucciones_bot
            )
            respuesta_final = response.text
            st.markdown(respuesta_final)
            st.session_state.messages.append({"role": "assistant", "content": respuesta_final})
        except Exception as e:
            # Mostramos el error espec铆fico para identificar si es un tema de clave o red
            st.error(f"Error de conexi贸n con el servidor: {e}")