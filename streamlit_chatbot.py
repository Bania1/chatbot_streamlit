from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate
import streamlit as st 

# Configuracion de la pagina de la app
st.set_page_config(page_title="Mi primer Chatbot", page_icon="☝️")
st.title("☝️ Chatbot Basico con langchain")
st.markdown("Este Chatbot está hecho con Langchain + Streamlit. ¡Escribe tu mensaje para comenzar!")

# Generar el sidebar para ajustar temperatura y seleccionar modelo
with st.sidebar:
    st.header("Configuración")
    temperature = st.slider("Temperatura", 0.0, 1.0, 0.5, 0.1)
    model_name = st.selectbox("Modelo", ["gpt-3.5-turbo", "gpt-4", "gpt-4o-mini"])
    
    # ¡Nuevo! Personalidad configurable
    personalidad = st.selectbox(
        "Personalidad del asistente",
        [
            "Útil y amigable",
            "Profesional y formal",
            "Casual y relajado",
            "Experto técnico",
            "Creativo y divertido"
        ]
    )

    # Recrear el modelo con los nuevos parametros
    chat_model = ChatOpenAI(model=model_name, temperature=temperature)

    # Definir mensajes del sistema según personalidad
    system_messages = {
        "Útil y amigable": "Eres un asistente útil y amigable llamado WikiBot Pro. Responde de manera clara y concisa.",
        "Profesional y formal": "Eres un asistente profesional y formal. Proporciona respuestas precisas y bien estructuradas.",
        "Casual y relajado": "Eres un asistente casual y relajado. Habla de forma natural y amigable, como un buen amigo.",
        "Experto técnico": "Eres un asistente experto técnico. Proporciona respuestas detalladas con precisión técnica.",
        "Creativo y divertido": "Eres un asistente creativo y divertido. Usa analogías, ejemplos creativos y mantén un tono alegre."
    }

 # NUEVO: ChatPromptTemplate con personalidad dinámica
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", system_messages[personalidad]),
        ("human", "Historial de conversación:\n{historial}\n\nPregunta actual: {mensaje}")
    ])

# # Crear el template de prompt con comportamiento especifico
# chat_prompt = ChatPromptTemplate.from_messages([
#     # Mensaje del sistema - Define la personalidad una sola vez
#     ("system", "Eres un asistente útil y amigable llamado WikiBot Pro. Responde de una manera clara y concisa."),
    
#     # El historial y el mensaje actual - se manejan como texto formateado
#     ("human", "Historial de conversación:\n{historial}\n\nPregunta actual: {mensaje}")
# ])

# prompt_template = PromptTemplate(
#     input_variables=["mensaje", "historial"],
#     template="""Eres un asistente util y amigable llamado WikiBot Pro.

# Historial de conversación:
# {historial}

# Responde de manera clara y concisa a la peteción: {mensaje}"""
# )

# Crear cadena usando LCEL (LangChain Expression Language)
cadena = chat_prompt | chat_model

# Inicializar el historial de mensajes
if 'mensajes' not in st.session_state:
    st.session_state.mensajes = []

# Mostrar mensajes previos en la interfaz, Renderizar historial existente
for msg in st.session_state.mensajes:
    if isinstance(msg, SystemMessage):
        # No muestro el mensaje por pantalla
        continue
    
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(role):
        st.markdown(msg.content)

if st.button("✏️​ Nueva conversación"):
    st.session_state.mensajes = []
    st.rerun()

# Cuadro de entrada de texto de usuario
pregunta = st.chat_input("Escribe tu mensaje: ")

if pregunta:
    # Mostrar y almacenar el mensaje del usuario
    with st.chat_message("user"):
        st.markdown(pregunta)
        
    # Preparar historial como texto
    historial_texto = ""
    for msg in st.session_state.mensajes[-10:]: # Últimos 10 mensajes
        if isinstance(msg, HumanMessage):
            historial_texto += f"Usuario: {msg.content}\n"
        elif isinstance(msg, AIMessage):
            historial_texto += f"Asistente: {msg.content}\n"
            
    if not historial_texto:
        historial_texto = "(No hay historial previo)"
    
    # Generar y mostrar respuesta del asistente
    try:
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""
            
            # Streaming de la respuesta
            for chunk in cadena.stream({"mensaje": pregunta, "historial": st.session_state.mensajes}):
                full_response += chunk.content # type: ignore
                response_placeholder.markdown(full_response + "✒️ ")
            
            response_placeholder.markdown(full_response)
            
        st.session_state.mensajes.append(HumanMessage(content=pregunta))
        st.session_state.mensajes.append(AIMessage(content=full_response))
        
    except Exception as e:
        st.error(f"Error al generar respuesta: {str(e)}")
        st.info("Verifica que tu API Key de OpenAI esté configurada correctamente.")
                    
    # # Almacenamos el mensaje en la memoria de streamlit
    # st.session_state.mensajes.append(HumanMessage(content=pregunta))
    
    # # Generar respuesta usando el modelo de lenguaje
    # respuesta = chat_model.invoke(st.session_state.mensajes)

    # # Mostrar la respuesta en la interfaz
    # with st.chat_message("assistant"):
    #     st.markdown(respuesta.content)
        
    # st.session_state.mensajes.append(respuesta)