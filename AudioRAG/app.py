import streamlit as st
import cohere
from data_ingestion import create_chunks
import embeddings as emd
from prompt_eng import build_prompt,generate_response, search_word_in_sentence
import torch
from speechbrain.inference.TTS import Tacotron2
from speechbrain.inference.vocoders import HIFIGAN
from transformers import pipeline
import pyaudio
import numpy as np
import torchaudio
import io
import re
from gtts import gTTS

def is_speech(audio_np,threshold=0.005):
    """Check if the audio contains speech based on RMS energy."""
    rms = np.sqrt(np.mean(audio_np**2))
    return rms > threshold

# Check for available device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

@st.cache_resource
def load_models():
    embedding_model = emd.load_model('BAAI/bge-small-en-v1.5')
    tacotron2 = Tacotron2.from_hparams(source="speechbrain/tts-tacotron2-ljspeech", savedir="tmpdir_tts", run_opts={"device": device})
    hifi_gan = HIFIGAN.from_hparams(source="speechbrain/tts-hifigan-ljspeech", savedir="tmpdir_vocoder", run_opts={"device": device})
    pipe_sr = pipeline("automatic-speech-recognition", model="openai/whisper-small",device=device)
    return embedding_model,tacotron2,hifi_gan,pipe_sr

embedding_model,tacotron2,hifi_gan,pipe_sr = load_models()
co = cohere.Client("905uGTlS9A4Yt5wcUYawV23b9nLPJRjnxv7FCd3w")

# Set up PyAudio for real-time streaming
p = pyaudio.PyAudio()
CHUNK = 32000  # Number of samples per frame
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

stream = p.open(format=FORMAT,
                 channels=CHANNELS,
                 rate=RATE,
                 input=True,
                 frames_per_buffer=CHUNK)

st.title("Chat With Docs")
uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type="pdf")
if uploaded_file is not None:
    print("here")
    if 'df' not in st.session_state:
        # Create chunks of the file
        chunks = create_chunks(uploaded_file)
        df = emd.create_df(chunks,embedding_model)
        st.session_state.df = df

col1, col2 = st.columns([4,1])
with col1:
    search_query = st.text_area(label = "input",label_visibility="collapsed",placeholder="Enter a question")
with col2:
    start_button = st.button(" 🎙️\n Start Listening ")
    stop_button = st.button(" 🛑 \n Stop Listening")


transcription_placeholder = st.empty()

if 'full_transcription' not in st.session_state:
    st.session_state.full_transcription = ""

if start_button:
    st.write("Listening... Speak into your microphone.")
    try:
        while not stop_button:
            # Read audio stream data
            audio_data = stream.read(CHUNK)
            audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0

            if is_speech(audio_np):
                # Perform speech recognition
                result = pipe_sr(audio_np, return_timestamps=False)
                new_text = result['text']
                
                # Append new text to the ongoing transcription
                st.session_state.full_transcription += " " + new_text

                transcription_placeholder.text(st.session_state.full_transcription)

            

            
    except KeyboardInterrupt:
        print("Stopping the speech recognition...")
        stream.stop_stream()
        stream.close()
        p.terminate()

if stop_button:
    st.write(st.session_state.full_transcription)
    query = st.session_state.full_transcription
    st.session_state.full_transcription = ""

    embedded_query = embedding_model.encode(search_word_in_sentence(query,["summary","summarize"]))
    top_k = emd.calculate_cosine_similarity(st.session_state.df,embedded_query)
    prompt = build_prompt(query,top_k)
    response = generate_response(co,prompt)
    st.write(response)
    if response:
        with st.spinner("Generating speech..."):
            # Generate speech using Google TTS
            tts = gTTS(text=response, lang="en", slow=False)
            # Save the generated speech to a byte stream
            audio_buffer = io.BytesIO()
            tts.save("temp_audio.mp3")  # Save to a file (optional)
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)  # Reset the buffer position to the beginning

            # Play the generated speech in Streamlit
            st.audio(audio_buffer, format="audio/mp3",autoplay=True)

        
    

if st.button("Search"):
    print(search_query)
    embedded_query = embedding_model.encode(search_word_in_sentence(search_query,["summary","summarize"]))
    top_k = emd.calculate_cosine_similarity(st.session_state.df,embedded_query)
    prompt = build_prompt(search_query,top_k)
    st.write(generate_response(co,prompt))

if st.sidebar.button('Reset PDF'):
    if 'df' in st.session_state:
        del st.session_state['df']  # Remove the stored dataframe        
    st.sidebar.write("PDF reset successfully!")

