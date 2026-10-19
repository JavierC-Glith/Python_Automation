import streamlit as st
import os
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

load_dotenv(find_dotenv(), override=True)

apiKey = os.environ.get('OPENAI_API_KEY')

client = OpenAI(api_key=apiKey)

#Opciones de voz
voices = ["alloy","echo", "fable", "onyx", "nova", "shimmer"]

st.title("Genrador de Audio con OpenAI")

text = st.text_area("Ingrese el texto", height=200)

voice = st.selectbox("Seleccione la voz: ", voices)

if st.button("Generar audio"):
    if text:
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text
        )
        audio_path= "audio.mp3"
        with open(audio_path, "wb") as output_file:
            for chunk in response.iter_bytes():
                if chunk:
                    output_file.write(chunk)

        st.success(f"Audio generado y guardado como {audio_path}")

        audio_file = open(audio_path, 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mp3')
    else: 
        st.error("Por favor, ingrese un texto.")