import streamlit as st
import google.generativeai as genai
import os
import random

# 1. Configuración de la página web
st.set_page_config(
    page_title="Chatbot Gimnasio Obregón",
    page_icon="GO",
    layout="wide"
)

# Estilo sobrio en azul suave y blanco
st.markdown("""
    <style>
        .stApp {
            background-color: #ffffff;
            color: #1e293b;
        }
        .header-sobrio {
            background-color: #f0f5fa;
            border: 1px solid #d6e4f0;
            border-left: 5px solid #2b6cb0;
            padding: 1.1rem 1.4rem;
            border-radius: 10px;
            margin-bottom: 1rem;
        }
        .header-sobrio h1 {
            color: #1e3a5f;
            margin: 0;
            font-size: 1.75rem;
        }
        .header-sobrio p {
            color: #475569;
            margin: 0.35rem 0 0 0;
        }
        .versiculo-sobrio {
            background-color: #f8fafc;
            border: 1px solid #dbeafe;
            border-left: 4px solid #3b82f6;
            padding: 0.85rem 1rem;
            border-radius: 8px;
            color: #1e293b;
            font-size: 0.95rem;
            line-height: 1.45;
            margin-top: 0.4rem;
        }
        [data-testid="stChatMessage"] {
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 0.25rem 0.5rem;
        }
    </style>
""", unsafe_allow_html=True)

# Amplia lista de versículos (puedes sumar o quitar los que desees)
versiculos = [
    ("Proverbios 22:6", "Guiar a los jóvenes por el buen camino ayuda a que no se aparten de él al crecer."),
    ("Filipenses 4:13", "Todo se puede afrontar con fortaleza cuando se confía en Dios."),
    ("Salmos 37:5", "Encomendar los planes a Dios y confiar en su guía trae respaldo en el camino."),
    ("Proverbios 4:7", "Buscar sabiduría y comprensión es fundamental para tomar buenas decisiones."),
    ("Santiago 1:5", "Pedir sabiduría con sencillez ayuda a discernir lo correcto en cada situación."),
    ("Josué 1:9", "Mantener el ánimo y la valentía fortalece para avanzar sin temor."),
    ("Proverbios 3:5-6", "Confiar de corazón y reconocer su dirección endereza los pasos."),
    ("Salmos 119:105", "La palabra de Dios ilumina el camino y da claridad en medio de las dudas."),
    ("Colosenses 3:23", "Hacer cada tarea de corazón y con esmero honra el esfuerzo diario."),
    ("Proverbios 16:3", "Poner las obras en manos de Dios afirma los proyectos y propósitos."),
    ("Mateo 5:16", "Actuar con buenas obras permite que otros reconozcan el bien en la comunidad."),
    ("Proverbios 1:5", "Escuchar con atención y buscar consejo permite ganar mayor sabiduría y dirección."),
    ("Proverbios 2:6", "La verdadera sabiduría, el conocimiento y el discernimiento provienen de Dios."),
    ("Proverbios 9:10", "El respeto reverente a Dios es el inicio de la sabiduría y el conocimiento."),
    ("Proverbios 13:20", "Caminar con personas sabias ayuda a crecer y a formar buen criterio."),
    ("Proverbios 15:14", "Una mente dispuesta a aprender busca conocimiento con interés y apertura."),
    ("Proverbios 18:15", "Quien es prudente adquiere conocimiento y el oído de los sabios busca saber."),
    ("Proverbios 19:20", "Aceptar el consejo y la instrucción ayuda a ser más sabio a lo largo de la vida."),
    ("Salmos 119:99", "Reflexionar en las enseñanzas de Dios da mayor entendimiento en el camino."),
    ("Eclesiastés 7:12", "La sabiduría protege y da vida a quienes la buscan con sinceridad."),
    ("Daniel 1:17", "Dios concede conocimiento, inteligencia y discernimiento para cada etapa de formación."),
    ("Proverbios 12:24", "La diligencia y el trabajo constante abren puertas y traen buenos resultados."),
    ("Proverbios 13:4", "El esfuerzo perseverante de quienes trabajan con dedicación es recompensado."),
    ("Proverbios 21:5", "Planificar con cuidado y trabajar con constancia conduce a buenos frutos."),
    ("1 Corintios 15:58", "Mantenerse firmes y trabajar con ánimo siempre tiene sentido en el propósito de Dios."),
    ("Gálatas 6:9", "No cansarse de hacer el bien a su tiempo traerá cosecha cuando se persevera."),
    ("2 Timoteo 1:7", "Dios da un espíritu de fortaleza, amor y dominio propio, no de temor."),
    ("Jeremías 29:11", "Dios tiene planes de bienestar y futuro para dar esperanza."),
    ("Salmos 90:17", "Pedir la gracia de Dios afirma la labor de nuestras manos y nuestro esfuerzo."),
    ("Romanos 12:2", "Renovar la mente ayuda a discernir lo bueno, agradable y perfecto."),
    ("Filipenses 3:14", "Avanzar con enfoque hacia la meta impulsa a seguir creciendo cada día."),
    ("Proverbios 15:1", "Una respuesta serena calma la tensión, mientras que una palabra dura aviva el conflicto."),
    ("Proverbios 17:17", "Un amigo verdadero acompaña en todo tiempo y brinda apoyo sincero."),
    ("Efesios 4:2", "Actuar con humildad, mansedumbre y paciencia fortalece la convivencia diaria."),
    ("Efesios 4:32", "Ser bondadosos, compasivos y perdonar de corazón construye comunidad."),
    ("Colosenses 3:12", "Vestirse de compasión, bondad, humildad, mansedumbre y paciencia embellece las relaciones."),
    ("Colosenses 3:14", "El amor une y da armonía duradera entre las personas."),
    ("Romanos 12:18", "Buscar la paz y la sana convivencia con todos es un llamado constante."),
    ("Salmos 34:14", "Apartarse del mal, hacer el bien y buscar la paz trae bienestar."),
    ("Isaías 41:10", "No temer ni desmayar, porque el respaldo y la ayuda de Dios sostienen."),
    ("Salmos 46:1", "Dios es refugio y fortaleza, una ayuda presente en momentos difíciles."),
    ("Salmos 23:1", "Contar con el cuidado y la guía de Dios brinda paz y provisión.")
]

if "versiculo_actual" not in st.session_state:
    st.session_state.versiculo_actual = random.choice(versiculos)

# 2. Barra lateral: imagen, rotación de versículos y limpieza de chat
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png", caption="Gimnasio Obregón", use_container_width=True)
    else:
        st.caption("Agrega `logo.png` en la carpeta del proyecto para mostrar tu imagen.")

    st.subheader("Versículo del día✨")
    cita, texto_versiculo = st.session_state.versiculo_actual
    st.markdown(
        f'<div class="versiculo-sobrio">“{texto_versiculo}”<br><strong>— {cita}</strong></div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Otro versículo", use_container_width=True):
            opciones = [v for v in versiculos if v != st.session_state.versiculo_actual]
            st.session_state.versiculo_actual = random.choice(opciones)
            st.rerun()
    with col2:
        if st.button("Limpiar chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

# 3. Encabezado principal
st.markdown("""
    <div class="header-sobrio">
        <h1>Chatbot Gimnasio Obregón</h1>
        <p>Consulta horarios, calendario, convivencia y normatividad.</p>
    </div>
""", unsafe_allow_html=True)

# 4. Conexión con la API de Google
api_key = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Por favor, configura la variable GEMINI_API_KEY en Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# 5. Cargar información del colegio
def cargar_informacion():
    if os.path.exists("informacion.txt"):
        with open("informacion.txt", "r", encoding="utf-8") as f:
            return f.read()
    return "No hay información disponible del colegio."

contexto_colegio = cargar_informacion()

# 6. Historial de mensajes
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hola, bienvenido al asistente virtual del **Gimnasio Obregón**. ¿En qué te puedo orientar hoy?"
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. Respuesta del bot
if user_question := st.chat_input("Escribe tu pregunta sobre el colegio..."):
    st.session_state.messages.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)

    instrucciones_bot = f"""
    Eres un asistente virtual amable y claro del colegio Gimnasio Obregón. Responde la pregunta basándote ÚNICAMENTE en la siguiente información oficial. Si la respuesta no aparece en el texto, indica con amabilidad que no cuentas con esa información.

    Información del colegio:
    {contexto_colegio}

    Pregunta del estudiante: {user_question}
    """

    with st.chat_message("assistant"):
        try:
            model = genai.GenerativeModel("gemini-3.6-flash")
            response = model.generate_content(instrucciones_bot)
            respuesta_final = response.text

            st.markdown(respuesta_final)
            st.session_state.messages.append({"role": "assistant", "content": respuesta_final})
        except Exception as e:
            st.error(f"Error de conexión con el servidor: {e}")
