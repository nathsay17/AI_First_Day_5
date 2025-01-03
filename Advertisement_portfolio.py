import os
import openai
import numpy as np
import pandas as pd
import json
import base64
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import CSVLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from openai.embeddings_utils import get_embedding
import faiss
import streamlit as st
import warnings
from streamlit_option_menu import option_menu
from streamlit_extras.mention import mention
from strings import home_string, System_Prompt
from background import apply_background,tint

warnings.filterwarnings("ignore")

st.set_page_config(page_title="Eve", page_icon="🤖", layout="wide")

#Background
def get_base64_image(image_path):
    with open(image_path, "rb") as file:
        encoded_image = base64.b64encode(file.read()).decode()
    return encoded_image

bg1 = get_base64_image("images/walle.jpg")
bg2 = get_base64_image("images/walle_and_eve.jpg")
bg3 = get_base64_image("images/eve.jpg")



with st.sidebar :
    st.image('images/mo.png')
    
    openai.api_key = st.text_input('Enter OpenAI API token:', type='password')
    if not (openai.api_key.startswith('sk-') and len(openai.api_key)==164):
        st.warning('Please enter your OpenAI API token!', icon='⚠️')
    else:
        st.success('Proceed to entering your prompt message!', icon='👉')
    with st.container() :
        l, m, r = st.columns((1, 3, 1))
        with l : st.empty()
        with m : st.empty()
        with r : st.empty()

    options = option_menu(
        "Content", 
        ["Home", "Data Set", "Talk to Eve"],
        icons = ['heart', 'clipboard', 'chat'],
        menu_icon = "book", 
        default_index = 0,
        styles = {
            "icon" : {"color" : "#ffffff", "font-size" : "20px"},
            "nav-link" : {"font-size" : "17px", "text-align" : "left", "margin" : "5px", "--hover-color" : "#354373"},
            "nav-link-selected" : {"background-color" : "#1b8cc4"}          
        }
    )
    st.image('images/axiom.png')

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_session" not in st.session_state:
    st.session_state.chat_session = None #Placeholder for your chat session initialization


if options == "Home":
    st.markdown(apply_background(bg1), unsafe_allow_html=True)
    st.markdown(home_string, unsafe_allow_html=True)

elif options == "Data Set":
    st.markdown(apply_background(bg2), unsafe_allow_html=True)
    st.markdown('<h1 class="outlined-text"></h1>', unsafe_allow_html=True)
    st.markdown(tint, unsafe_allow_html=True)
    
    dataframed = pd.read_csv('WallEve_dataset.csv')
    html_table = dataframed.to_html(classes='custom-table', escape=False)
    st.markdown(html_table, unsafe_allow_html=True)

elif options == "Talk to Eve":
    st.markdown(apply_background(bg3), unsafe_allow_html=True)
    st.markdown('<h1 class="outlined-text">Talk to Eve</h1>', unsafe_allow_html=True)
    dataframed = pd.read_csv('WallEve_dataset.csv')
    dataframed['combined'] = dataframed.apply(lambda row : ' '.join(row.values.astype(str)), axis = 1)
    documents = dataframed['combined'].tolist()
    embeddings = [get_embedding(doc, engine = "text-embedding-3-small") for doc in documents]
    embedding_dim = len(embeddings[0])
    embeddings_np = np.array(embeddings).astype('float32')
    index = faiss.IndexFlatL2(embedding_dim)
    index.add(embeddings_np)    
    
    def initialize_conversation(prompt):
     if 'messagess' not in st.session_state:
         st.session_state.messagess = []
         st.session_state.messagess.append({"role": "system", "content": System_Prompt})
         chat =  openai.ChatCompletion.create(model = "gpt-4o-mini", messages = st.session_state.messagess, temperature=0.5, max_tokens=1500, top_p=1, frequency_penalty=0, presence_penalty=0)
         response = chat.choices[0].message.content
         st.session_state.messagess.append({"role": "assistant", "content": response})
    
    initialize_conversation(System_Prompt)
    
    for messages in st.session_state.messagess :
      if messages['role'] == 'system' : continue 
      else :
        with st.chat_message(messages["role"]):
             st.markdown(messages["content"])
    
    if user_message := st.chat_input("Say something"):
     with st.chat_message("user"):
          st.markdown(user_message)
     query_embedding = get_embedding(user_message, engine='text-embedding-3-small')
     query_embedding_np = np.array([query_embedding]).astype('float32')
     _, indices = index.search(query_embedding_np, 2)
     retrieved_docs = [documents[i] for i in indices[0]]
     context = ' '.join(retrieved_docs)
     structured_prompt = f"Context:\n{context}\n\nQuery:\n{user_message}\n\nResponse:"
     chat =  openai.ChatCompletion.create(model = "gpt-4o-mini", messages = st.session_state.messagess + [{"role": "user", "content": structured_prompt}], temperature=0.5, max_tokens=1500, top_p=1, frequency_penalty=0, presence_penalty=0)
     st.session_state.messagess.append({"role": "user", "content": user_message})
     response = chat.choices[0].message.content
     with st.chat_message("assistant"):
          st.markdown(response)
     st.session_state.messagess.append({"role": "assistant", "content": response})
    
