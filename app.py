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
    versiculos_colegio = [
    ("Proverbios 22:6", "Dirige a tus hijos por el camino correcto, y cuando sean mayores, no lo abandonarán."),
    ("Filipenses 4:13", "Pues todo lo puedo hacer por medio de Cristo, quien me da las fuerzas."),
    ("Salmos 37:5", "Entrega al Señor todo lo que haces; confía en él, y él te ayudará."),
    ("Proverbios 4:7", "¡Adquirir sabiduría es lo más sabio que puedes hacer! Y en todo lo demás que hagas, desarrolla buen juicio."),
    ("Santiago 1:5", "Si necesitan sabiduría, pídansela a nuestro generoso Dios, y él se la dará; no los reprenderá por pedirla."),
    ("Josué 1:9", "Mi mandato es: “¡Sé fuerte y valiente! No tengas miedo ni te desanimes, porque el Señor tu Dios está contigo dondequiera que vayas”."),
    ("Proverbios 3:5-6", "Confía en el Señor con todo tu corazón; no dependas de tu propio entendimiento. Busca su voluntad en todo lo que hagas, y él te mostrará cuál camino tomar."),
    ("Salmos 119:105", "Tu palabra es una lámpara que guía mis pies y una luz para mi camino."),
    ("Colosenses 3:23", "Trabajen de buena gana en todo lo que hagan, como si fuera para el Señor y no para la gente."),
    ("Proverbios 16:3", "Pon todo lo que hagas en manos del Señor, y tus planes tendrán éxito."),
    ("Mateo 5:16", "De la misma manera, dejen que sus buenas acciones brillen a la vista de todos, para que todos alaben a su Padre celestial."),
    ("Proverbios 1:5", "Que los sabios escuchen estos proverbios y se hagan aún más sabios. Que los que tienen entendimiento reciban dirección"),
    ("Proverbios 2:6", "¡Pues el Señor concede la sabiduría! De su boca provienen el saber y el entendimiento."),
    ("Proverbios 9:10", "El temor del Señor es la base de la sabiduría. El conocimiento del Santo da por resultado el buen juicio."),
    ("Proverbios 13:20", "Camina con sabios y te harás sabio; júntate con necios y te meterás en dificultades."),
    ("Proverbios 15:14", "El sabio tiene hambre de conocimiento, mientras que el necio se alimenta de basura."),
    ("Proverbios 18:15", "Las personas inteligentes están siempre dispuestas a aprender; tienen los oídos abiertos al conocimiento."),
    ("Proverbios 19:20", "Consigue todo el consejo y la instrucción que puedas, para que seas sabio por el resto de tu vida."),
    ("Salmos 119:99", "Tengo más entendimiento que todos mis maestros, porque vivo pensando en tus leyes."),
    ("Eclesiastés 7:12", "La sabiduría y el dinero pueden abrir casi todas las puertas, pero solo la sabiduría puede salvarle la vida al que la tiene."),
    ("Daniel 1:17", "A estos cuatro jóvenes Dios les dio aptitud excepcional para comprender todos los aspectos de la literatura y la sabiduría. Y a Daniel Dios le dio la capacidad especial de interpretar el significado de visiones y sueños."),
    ("Proverbios 12:24", "Los que trabajan duro llegarán a ser líderes; los perezosos serán esclavos."),
    ("Proverbios 13:4", "Los perezosos ambicionan mucho y obtienen poco, pero los que trabajan con esmero prosperarán."),
    ("Proverbios 21:5", "Los planes bien pensados y el arduo trabajo llevan a la prosperidad, pero los atajos tomados a la carrera conducen a la pobreza."),
    ("1 Corintios 15:58", "Por lo tanto, mis amados hermanos, permanezcan fuertes y constantes. Trabajen siempre para el Señor con entusiasmo, porque ustedes saben que nada de lo que hacen para el Señor es inútil."),
    ("Gálatas 6:9", "Así que no nos cansemos de hacer el bien. A su debido tiempo, cosecharemos numerosas bendiciones si no nos damos por vencidos."),
    ("2 Timoteo 1:7", "Pues Dios no nos ha dado un espíritu de temor y timidez, sino de poder, amor y autodisciplina."),
    ("Jeremías 29:11", "Pues yo sé los planes que tengo para ustedes —dice el Señor—. Son planes para lo bueno y no para lo malo, para darles un futuro y una esperanza."),
    ("Salmos 90:17", "Y que el Señor nuestro Dios nos dé su aprobación y haga que nuestros esfuerzos tengan éxito. ¡Sí, haz que nuestros esfuerzos tengan éxito!"),
    ("Romanos 12:2", "No imiten las conductas ni las costumbres de este mundo, más bien dejen que Dios los transforme en personas nuevas al cambiarles la manera de pensar. Entonces aprenderán a conocer la voluntad de Dios para ustedes, la cual es buena, agradable y perfecta."),
    ("Filipenses 3:14", "Avanzo hacia la meta para poder llevarme el premio celestial al cual Dios nos llama por medio de Cristo Jesús."),
    ("Proverbios 15:1", "La respuesta apacible desvía el enojo, pero las palabras ásperas encienden los ánimos."),
    ("Proverbios 17:17", "Un amigo es siempre leal, y un hermano nace para ayudar en tiempo de necesidad."),
    ("Efesios 4:2", "Sean siempre humildes y amables. Sean pacientes unos con otros y tolérense las faltas por amor."),
    ("Efesios 4:32", "Por el contrario, sean amables unos con otros, sean de buen corazón, y perdónense unos a otros, tal como Dios los ha perdonado a ustedes por medio de Cristo."),
    ("Colosenses 3:12", "Dado que Dios los eligió para que sean su pueblo santo y amado por él, ustedes tienen que vestirse de tierna compasión, bondad, humildad, gentileza y paciencia."),
    ("Colosenses 3:14", "Sobre todo, vístanse de amor, lo cual nos une a todos en perfecta armonía."),
    ("Romanos 12:18", "Hagan todo lo posible por vivir en paz con todos."),
    ("Salmos 34:14", "¡Apártate de la maldad y haz el bien! Busca la paz y esfuérzate por mantenerla."),
    ("Isaías 41:10", "No tengas miedo, porque yo estoy contigo; no te desalientes, porque yo soy tu Dios. Te daré fuerzas y te ayudaré; te sostendré con mi mano derecha victoriosa."),
    ("Salmos 46:1", "Dios es nuestro refugio y nuestra fuerza, siempre está dispuesto a ayudar en tiempos de dificultad."),
    ("Proverbios 10:17", "Los que aceptan la disciplina van por el camino que lleva a la vida, pero los que no hacen caso de la corrección se descarriarán."),
    ("Proverbios 11:14", "Sin liderazgo sabio, la nación se hunde; la seguridad está en tener muchos consejeros."),
    ("Proverbios 12:1", "Para aprender, hay que amar la disciplina; es tonto despreciar la corrección."),
    ("Proverbios 14:23", "El trabajo duro siempre produce ganancias, pero el mucho hablar lleva a la pobreza."),
    ("Proverbios 16:9", "Podemos hacer nuestros planes, pero el Señor determina nuestros pasos."),
    ("Proverbios 16:16", "¡Cuánto mejor es adquirir sabiduría que oro, y el buen juicio que la plata!"),
    ("Proverbios 17:22", "El corazón alegre es una buena medicina, pero el espíritu quebrantado consume las fuerzas."),
    ("Proverbios 18:10", "El nombre del Señor es una fortaleza firme; los justos corren a él y quedan a salvo."),
    ("Proverbios 20:11", "Aun a los niños se les conoce por su forma de actuar, si su conducta es pura y correcta."),
    ("Proverbios 24:3-4", "Con sabiduría se edifica una casa, y con inteligencia se echan los cimientos. Con conocimiento se llenan sus cuartos de toda clase de riquezas y objetos valiosos."),
    ("Salmos 1:1-2", "Qué alegría para los que no siguen el consejo de malos, ni andan con pecadores, ni se juntan con burlones; sino que se deleitan en la ley del Señor meditando en ella día y noche."),
    ("Salmos 19:14", "Que las palabras de mi boca y la meditación de mi corazón sean de tu agrado, oh Señor, mi roca y mi redentor."),
    ("Salmos 25:4-5", "Muéstrame el camino correcto, oh Señor; señálame la senda que debo seguir. Guíame con tu verdad y enséñame, porque tú eres el Dios que me salva. Todo el día pongo en ti mi esperanza."),
    ("Salmos 27:1", "El Señor es mi luz y mi salvación, entonces ¿por qué habría de temer? El Señor es mi fortaleza y me protege del peligro, entonces ¿por qué habría de temblar?"),
    ("Salmos 32:8", "El Señor dice: «Te guiaré por el mejor sendero para tu vida; te aconsejaré y velaré por ti."),
    ("Salmos 86:11", "Enséñame tus caminos, oh Señor, para que viva de acuerdo con tu verdad! Concédeme pureza de corazón, para que te honre."),
    ("Salmos 139:23-24", "Examíname, oh Dios, y conoce mi corazón; pruébame y conoce los pensamientos que me inquietan. Señálame cualquier cosa en mí que ofenda y guíame por el camino de la vida eterna."),
    ("Isaías 30:21", "Tus propios oídos lo oirán. Detrás de ti una voz dirá: «Este es el camino por el que debes ir», ya sea a la derecha o a la izquierda."),
    ("Isaías 40:31", "En cambio, los que confían en el Señor encontrarán nuevas fuerzas; volarán alto, como con alas de águila. Correrán y no se cansarán; caminarán y no desmayarán."),
    ("Miqueas 6:8", "¡No, oh pueblo! El Señor te ha dicho lo que es bueno, y lo que él exige de ti: que hagas lo que es correcto, que ames la compasión y que camines humildemente con tu Dios."),
    ("Mateo 7:24", "Todo el que escucha mi enseñanza y la sigue es sabio, como la persona que construye su casa sobre una roca sólida."),
    ("Lucas 11:28", "Jesús respondió: —Aún más benditos son todos los que oyen la palabra de Dios y la ponen en práctica."),
    ("Juan 8:31-32", "Jesús les dijo a los judíos que habían creído en él: —Ustedes son verdaderamente mis discípulos si se mantienen fieles a mis enseñanzas; y conocerán la verdad, y la verdad los hará libres."),
    ("Juan 13:34", "Así que ahora les doy un nuevo mandamiento: ámense unos a otros. Tal como yo los he amado, ustedes deben amarse unos a otros."),
    ("Romanos 8:28", "Y sabemos que Dios hace que todas las cosas cooperen para el bien de quienes lo aman y son llamados según el propósito que él tiene para ellos."),
    ("Romanos 15:13", "Le pido a Dios, fuente de esperanza, que los llene completamente de alegría y paz, porque confían en él. Entonces rebosarán de una esperanza segura mediante el poder del Espíritu Santo."),
    ("1 Corintios 13:4-5", "El amor es paciente y bondadoso. El amor no es celoso ni fanfarrón ni orgulloso ni ofensivo. No exige que las cosas se hagan a su manera. No se irrita ni lleva un registro de las ofensas recibidas.")
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
