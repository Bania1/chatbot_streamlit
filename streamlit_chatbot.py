from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
import streamlit as st 

# Configuracion de la pagina de la app
st.set_page_config(page_title="Mi primer Chatbot", page_icon="☝️")
st.title("☝️ Chatbot Basico con langchain")
st.markdown("Chatbot hecho con Langchain + Streamlit. ¡Escribe tu mensaje para comenzar!")

chat_model = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)