from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.prompts import PromptTemplate
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

    # Recrear el modelo con los nuevos parametros
    chat_model = ChatOpenAI(model=model_name, temperature=temperature)


# Inicializar el historial de mensajes
if 'mensajes' not in st.session_state:
    st.session_state.mensajes = []

# Crear el template de prompt con comportamiento especifico
prompt_template = PromptTemplate(
    input_variables=["mensaje", "historial"],
    template="""Eres un asistente util y amigable llamado WikiBot Pro.

Historial de conversación:
{historial}

Responde de manera clara y concisa a la peteción: {mensaje}"""
)

# Crear cadena usando LCEL (LangChain Expression Language)
cadena = prompt_template | chat_model

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
    
    # Generar y mostrar respuesta del asistente
    try:
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""
            
            # Streaming de la respuesta
            for chunk in cadena.stream({"mensaje": pregunta, "historial": st.session_state.mensajes}):
                full_response += chunk.content
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