from collections import namedtuple
import altair as alt

import os, time
import pandas as pd
import math
import glob

from io import StringIO
import base64
import openai

# -------------IMPORTING CORE FUNCTIONALITIES OF THE SpeeKAR_BOT-------------
from innoguideGPT import (
    speechtotext,
    texttospeech_raw,
    extract_commands_from_text,
    answer_question
)


# -------------------AUDIO FUNCTIONALITY-------------------------
from mutagen.wave import WAVE

# --------------------HTML BUILDER AND FUNCTIONALITIES-----------------------------------#
from htbuilder import (
    HtmlElement,
    div,
    ul,
    li,
    br,
    hr,
    a,
    p,
    img,
    styles,
    classes,
    fonts,
)
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb

import streamlit as st
from audiorecorder import audiorecorder


from PIL import Image


# ------------------DEFAULTS--------------------#
LANGUAGE = "en"

SECRET_API_KEY = os.environ["SECRET_API_KEY"]
openai.api_key = SECRET_API_KEY





# -----------------------HELPER FUNCTIONS--------------------------#
def image(src_as_string, **style):
    return img(src=src_as_string, style=styles(**style))


def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)


def layout(*args):
    style = """
    <style>
      # MainMenu {visibility: display;}
      footer {visibility: display;}
     .stApp { bottom: 105px; }
    </style>
    """
    style_div = styles(
        position="fixed",
        left=0,
        bottom=0,
        margin=px(0, 50, 0, 50),
        width=percent(100),
        color="blue",
        text_align="left",
        height="auto",
        opacity=1,
    )

    style_hr = styles(
        display="block",
        margin=px(8, 8, "auto", "auto"),
        border_style="inset",
        border_width=px(1.5),
    )

    body = p()
    foot = div(style=style_div)(hr(style=style_hr), body)

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)

        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)


# -------------------------------FUNCTIONS FOR KAR BASED RESPONSE GENERATION-------------#
def process_query(speech_input, email, passwd):
    question0 = speech_input
    question = speech_input
    query = speechtotext(speech_input)

    # ans, context, keys = chatbot_slim(query, text_split)
    return query

# -------------------------------------------------------------------------#
# --------------------------GUI CONFIGS------------------------------------#
# -------------------------------------------------------------------------#
# App title
st.set_page_config(page_title="InnoGuideGPT")
st.header("InnoGuideGPT: Making navigation robots humanlike!")
st.title("Howdy! I am at your service! Where do you want to go?")


# Hugging Face Credentials
with st.sidebar:
    st.title("InnoGuideGPT")
    st.success(
        "Access to this Gen-AI Powered Chatbot is provided by  [Rahul](https://www.linkedin.com/in/rahul-sundar-311a6977/)!!",
        icon="✅",
    )
    hf_email = "rahul.sundar95@gmail.com"
    hf_pass = "PASS"
    st.markdown(
        "📖 This app is hosted by Rahul Sundar [website](https://github.com/RahulSundar)!"
    )
    image = Image.open("innoguideibotcfiiitmlogos/innoGuide_logo.jpg")
    st.image(
        image,
        caption=None,
        width=None,
        use_column_width=None,
        clamp=False,
        channels="RGB",
        output_format="auto",
    )


# ------------------------------------------------------------------------------#
# -------------------------QUERY AUDIO INPUT - RETURNING TEXT QUERY-------------#
# ------------------------------------------------------------------------------#
query_status = 0
text_input_status = 0
audio_input_status = 0
if query_status == 0 and text_input_status == 0:
    with st.chat_message("user"):
        query = st.text_area(label = "Let me know what you have in mind!")
    if query != "":
        query_status = 1
        text_input_status = 1
    if query == "":
        with st.chat_message("assistant"):
            st.write("You could choose to speak into the mic as well, if you wish!")

if query_status == 0 and audio_input_status == 0:
    audio = audiorecorder("Click to record", "Click to stop recording")            
    if not audio.empty():
        # To play audio in frontend:
        with st.chat_message("user"):
        
            
            st.audio(audio.export().read())
            # To save audio to a file, use pydub export method:
            audio.export("query.wav", format="wav")
            
            
        querywav = WAVE("query.wav")
        if querywav.info.length > 0:
            
            query = process_query("query.wav", hf_email, hf_pass)
            st.markdown(
                """
                <style>
                .big-font {
                    font-size:20px !important;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )
        
            query_status = 1
            audio_input_status = 1
        else:
            with st.chat_message("assistant"):
                st.write("Let me know if you have any questions!")
        


while (query_status == 1):
    
    with st.chat_message("assistant"):
        st.write("If I heard you right, your question is as follows ")
    with st.chat_message("user"):
        st.write(query)

    with st.chat_message("assistant"):    
        
        st.markdown(
                """
                    <style>
                    .big-font {
                        font-size:20px !important;
                    }
                    </style>
                    """,
                unsafe_allow_html=True,
            )
        answer=answer_question(query)            
        
        if (("take" or "go") in query.lower()) and ("i don't know" not in answer.lower()):
            
            json = extract_commands_from_text("Look at the query and answer below \n and appropriately generate the JSON object: " + query + answer)
            
            st.write(json)
            st.write(answer)
        # -----------text to speech--------------------------#
            texttospeech_raw(str(answer), language="en")
            audio_file = open("answer.wav", "rb")
            audio_bytes = audio_file.read()
            #st.audio(audio_bytes, format="audio/wav")
            mymidia_placeholder = st.empty()
            with open("answer.wav", "rb") as audio_file:
                #st.audio(audio_bytes, format="audio/wav")
                audio_bytes = audio_file.read()
                b64 = base64.b64encode(audio_bytes).decode()
                md = f"""
                     <audio controls autoplay="true">
                     <source src="data:audio/wav;base64,{b64}" type="audio/wav">
                     </audio>
                     """
                mymidia_placeholder.empty()
                time.sleep(1)
                mymidia_placeholder.markdown(md, unsafe_allow_html=True)
                
        elif (("take" or "go") not in query.lower()) and ("i don't know" not in answer.lower()):
            st.write(answer)
        # -----------text to speech--------------------------#
            texttospeech_raw(str(answer), language="en")
            audio_file = open("answer.wav", "rb")
            audio_bytes = audio_file.read()
            #st.audio(audio_bytes, format="audio/wav")
            mymidia_placeholder = st.empty()
            with open("answer.wav", "rb") as audio_file:
                #st.audio(audio_bytes, format="audio/wav")
                audio_bytes = audio_file.read()
                b64 = base64.b64encode(audio_bytes).decode()
                md = f"""
                     <audio controls autoplay="true">
                     <source src="data:audio/wav;base64,{b64}" type="audio/wav">
                     </audio>
                     """
                mymidia_placeholder.empty()
                time.sleep(1)
                mymidia_placeholder.markdown(md, unsafe_allow_html=True)
                
        elif (("take" or "go") in query.lower()) and ("i don't know" in answer.lower()):
        # -----------text to speech--------------------------#
            texttospeech_raw(str("Hey! Let me take you to these exhibits of your choice!"), language="en")
            audio_file = open("answer.wav", "rb")
            audio_bytes = audio_file.read()
            #st.audio(audio_bytes, format="audio/wav")
            mymidia_placeholder = st.empty()
            with open("answer.wav", "rb") as audio_file:
                #st.audio(audio_bytes, format="audio/wav")
                audio_bytes = audio_file.read()
                b64 = base64.b64encode(audio_bytes).decode()
                md = f"""
                     <audio controls autoplay="true">
                     <source src="data:audio/wav;base64,{b64}" type="audio/wav">
                     </audio>
                     """
                mymidia_placeholder.empty()
                time.sleep(1)
                mymidia_placeholder.markdown(md, unsafe_allow_html=True)


    query_status = 0
    text_input_status = 0
    audio_input_status = 0
   

def footer():
    myargs = [
        "Engineered in India",
        "" " with ❤️ by ",
        link("https://www.linkedin.com/in/rahul-sundar-311a6977/", "@RahulSundar"),
        link("https://github.com/GB2k4", "@GautamB"),
        link("https://github.com/Ishita1111", "@IshitaMittal"),
        link("https://github.com/TankalaSatyaSai", "@TankalaSatyasai"),
        br(),
        ", and",
        link("https://github.com/KineticKrishna", "@SaiKrishna")
    ]
    layout(*myargs)


footer()
