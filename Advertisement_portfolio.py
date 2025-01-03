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

warnings.filterwarnings("ignore")

# Function to load the CSV file
def load_csv():
    file_path = "path_to_your_github_repo/your_csv_file.csv"  # Path to CSV file in your GitHub repo
    df = pd.read_csv(file_path)
    return df

# Display images for the selected customer
def display_images_for_customer(customer_name, df):
    # Find the customer row based on their name
    customer_data = df[df['name'] == customer_name]
    if not customer_data.empty:
        # Assuming product columns are from the second column onward (product1 to product4)
        products = customer_data.iloc[0, 1:].values  # Get the products for the customer
        
        # Loop through the products and display images
        for product in products:
            if product != 'N/A':  # Skip 'N/A' values
                # Construct the image file path (assuming images are in the 'images' folder)
                image_path = os.path.join("images", f"{product}.png")  # Adjust extension if needed
                if os.path.exists(image_path):  # Ensure the image file exists
                    st.image(image_path, caption=product, use_column_width=True)
                else:
                    st.warning(f"Image for {product} not found.")
    else:
        st.warning(f"No data found for {customer_name}.")

st.set_page_config(page_title="Lazana", page_icon="🤖", layout="wide")

with st.sidebar :
    st.image('images/Lazana1.png')
    
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
        ["Home", "Data Set"],
        icons = ['heart', 'clipboard'],
        menu_icon = "book", 
        default_index = 0,
        styles = {
            "icon" : {"color" : "#ffffff", "font-size" : "20px"},
            "nav-link" : {"font-size" : "17px", "text-align" : "left", "margin" : "5px", "--hover-color" : "#354373"},
            "nav-link-selected" : {"background-color" : "#1b8cc4"}          
        }
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_session" not in st.session_state:
    st.session_state.chat_session = None #Placeholder for your chat session initialization


if options == "Home":
    st.markdown(home_string, unsafe_allow_html=True)

elif options == "Data Set":
    # Load the CSV file
    df = load_csv()

    # Customer buttons
    customer_names = ['Xyrel', 'Carlo', 'Amber', 'Danielle']
    for customer_name in customer_names:
        if st.button(customer_name):
            display_images_for_customer(customer_name, df)
