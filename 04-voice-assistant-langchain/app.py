from streamlit_mic_recorder import speech_to_text
from langchain_openai import ChatOpenAI
import streamlit as st

apenai_api_key = "Ingresar api de ChatGPT"

llm = ChatOpenAI(model="gpt-4o", openai_api_key=openai_api_key)

st.title("Tu asistente de voz todo en uno")
st.write("Aplicación de cha habilitada por voz")

text = speech_to_text(lenguage="es", use_container_width=True, just_once = False, key="STT")

if text:
    st.write("Tu: ",text)
    response = llm.invoke(text)
    st.write("Respuesta del modelo: ", response.content)