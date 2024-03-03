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
from langchain import hub
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
from langchain import PromptTemplate

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings
import numpy as np
import torch
import os
import yaml, json
from langchain.chat_models import ChatOpenAI
from langchain.chains import create_extraction_chain



# ----------DEFAULTS:------------#
LANGUAGE = "en"

SECRET_API_KEY = os.environ["SECRET_API_KEY"]
openai.api_key = SECRET_API_KEY





#----------------------------------------------------#


def extract_commands_from_text(text):
    '''commands: GO, STOP, WAIT,
    mode: speech conversation or command'''

    llm = ChatOpenAI(openai_api_key=openai.api_key, temperature=0, model="gpt-3.5-turbo")
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
        json.dump([input_data[0]], json_file)

    return input_data[0]



#-----------------------------------RAG Pipeline ----------------------------------------#
def answer_question(question):
    '''
    Given a index persisted from a prefed document, carry out your queries and generate answers using OpenAI's GPT3.5 API calls.
    '''
    embeddings= OpenAIEmbeddings(model="text-embedding-ada-002",openai_api_key=openai.api_key)
    db=FAISS.load_local(r"faiss_index1",embeddings)
    
    # LLM definition
    llm = OpenAI(openai_api_key=openai.api_key)
    
    #prompt engineering
    template = """
              You are a helpful assistant who answers question based on context provided: {context}

              If you don't have enough information to answer the question, say: "Sorry, I cannot answer that".

              """
    template = """
              You are a helpful assistant who answers question based on context provided: {context}

              If you don't have enough information to answer the question, say: "I cannot answer".

              """
    template = """ You answer question based on context below, and if question can't be answered based on context, say \"I don't know\"\n\nContext: {context} """

    system_message_prompt = SystemMessagePromptTemplate.from_template(template)

    # Human question prompt

    human_template = "Answer following question: {question}"

    template = """ Answer question {question} based on context below, and if question can't be answered based on context,
    say \"I don't know\"\n\nContext: {context}

    Answer:
    """

    template = """ Use following pieces of context to answer the question. Provide answer in full detail using provided context.
    If you don't know the answer, say I don't know
    {context}
    Question : {question}
    Answer:"""

    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chunk_size = 1500
    PROMPT = PromptTemplate(
        input_variables=["context", "question"], template=template
    )

    chain_type_kwargs = {"prompt": PROMPT}
    
    
    qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=db.as_retriever(),
    return_source_documents=True,
    chain_type_kwargs={"prompt": PROMPT},)
    
    res = qa_chain(question)
    
    return res["result"]


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

