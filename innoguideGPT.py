import time, os
import io
import scipy
import numpy as np

# ----------------SPEECH RECOGNITION /AUDIO/TEXT TO SPEECH DEPENDENCIES-------------#
from scipy.io.wavfile import read as wav_read
from pydub import AudioSegment
from pydub.playback import play
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
import speech_recognition as sr
import ffmpeg
from gtts import gTTS
import soundfile as sf

# ----STREAMLIT RELATED----#
import streamlit as st
import requests
import re
import urllib.request


# ---------DOCUMENT/WEBSITE PARSING---------#
from bs4 import BeautifulSoup
from collections import deque
from html.parser import HTMLParser
from urllib.parse import urlparse

# -------DATA FRAME/DOCX/TEXT HANDLING----------$
import pandas as pd
import pprint as pp
from docx import Document
from docx.shared import Inches
import textwrap
import glob

# -----------------------------------------------------------------------------------------#
# ---------------------------------OPENAI and LANGCHAIN DEPENDENCIES-----------------------#
# -----------------------------------------------------------------------------------------#
import openai
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI

# from langchain import HuggingFacePipeline
from langchain.llms.huggingface_pipeline import HuggingFacePipeline
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import UnstructuredWordDocumentLoader
from langchain.vectorstores import FAISS
from langchain.chains import LLMChain
from dotenv import find_dotenv, load_dotenv
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

import numpy as np
import torch
import os
import yaml, json
from langchain.chat_models import ChatOpenAI
from langchain.chains import create_extraction_chain
# --------------KEYBERT MODEL ---------------#
from keybert import KeyBERT



# ----------DEFAULTS:------------#
LANGUAGE = "en"

SECRET_API_KEY = os.environ["SECRET_API_KEY"]
openai.api_key = SECRET_API_KEY





#----------------------------------------------------#


def extract_commands_from_text(text):
    '''commands: GO, STOP, WAIT,
    mode: speech conversation or command'''

    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0, model="gpt-3.5-turbo")
    extraction_schema = {
        "properties":{
            "route":{"description": "list of exhibits to be visited.",
                     "type": "array",
                     "items":{
                                     "type":"integer"
                            }
                    },
        },"required":["route"]}

    
    extraction_chain = create_extraction_chain(extraction_schema, llm)
    inp = text
    input_data = extraction_chain.run(inp)

    current_directory = os.getcwd()
    file_name = "commandconfig.json"
    file_path = os.path.join(current_directory, file_name)

    with open(file_path, "w") as json_file:
        json.dump([input_data[0]], json_file, default_flow_style=False)

    return input_data[0]











# ----------------TEXT TO SPEECH FUNCTION FOR ANSWER READOUT---------#
def texttospeech_raw(text, language, savename="answer", slow=False):
    """
    This function here, calls the google text to speech engine to read out the answer generated by the KAR framework.
    """
    myobj = gTTS(text=text, lang=language, slow=False)

    # Saving the converted audio in a mp3 file
    myobj.save(savename + ".mp3")
    sound = AudioSegment.from_mp3(savename + ".mp3")
    sound.export(savename + ".wav", format="wav")


# ---------------SPEECH RECOGNITION---------#
def speechtotext(query_audio):
    """
    This function takes in a ".wav" audio file as input and converts into text.
    """
    r = sr.Recognizer()

    audio_ex = sr.AudioFile(query_audio)
    # type(audio_ex)

    # Create audio data
    with audio_ex as source:
        audiodata = r.record(audio_ex)
    # type(audiodata)
    # Extract text
    text = r.recognize_google(audio_data=audiodata, language="en-US")
    print("stotext ::", text)
    return text

