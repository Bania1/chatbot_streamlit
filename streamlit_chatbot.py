from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
import streamlit as st 

# Configuracion de la pagina de la app
st.set_page_config(page_title="Mi primer Chatbot", page_icon="☝️")
st.title("☝️ Chatbot Basico con langchain")
st.markdown("Chatbot hecho con Langchain + Streamlit. ¡Escribe tu mensaje para comenzar!")

chat_model = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)


# Inicializar el historial de mensajes
if 'mensajes' not in st.session_state:
    st.session_state.mensajes = []

# Mostrar mensajes previos en la interfaz
for msg in st.session_state.mensajes:
    if isinstance(msg, SystemMessage):
        # No muestro el mensaje por pantalla
        continue
    
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    
    with st.chat_message(role):
        st.markdown(msg.content)
        
# Cuadro de entrada de texto de usuario
pregunta = st.chat_input("Escribe tu mensaje: ")

if pregunta:
    # Mostrar inmediatamente el mensaje en la interfaz
    with st.chat_message("user"):
        st.markdown(pregunta)
        
    # Almacenamos el mensaje en la memoria de streamlit
    st.session_state.mensajes.append(HumanMessage(content=pregunta))
    
