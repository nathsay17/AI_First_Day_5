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

    
    # Function to load customer data from a CSV file
    def load_customer_data(file_path):
        # Load the CSV file into a pandas DataFrame
        df = pd.read_csv(file_path)
        return df
    
    # Simulated agents for customer, purchases, and categorization
    def customer_analyst(customer_name):
        # Placeholder function for analyzing customer data
        return f"Analyzing data for {customer_name}"
    
    def purchase_analyzer(customer_name, purchases):
        # Placeholder for analyzing purchases
        return [f"Analyzing purchases for {customer_name}: {', '.join(purchases)}"]
    
    def category_classifier(purchases):
        # Simulated categorization based on products
        categories = {
            "cat_bed": ["cat_bed", "cat_food"],
            "cat_collar": ["cat_collar"],
            "dog_food": ["dog_food"],
            "shoes_sneakers": ["shoes_sneakers", "shoes_boots"],
            "watch_regular": ["watch_regular"]
        }
        classified = []
        for category, items in categories.items():
            if any(item in purchases for item in items):
                classified.append(category)
        return classified
    
    def orchestrator(customer_name, classified_categories):
        # Orchestrator selects personalized ads based on categorized purchases
        ads = []
        for category in classified_categories:
            img_path = f"images/{category}.jpg"  # Example image path
            if os.path.exists(img_path):
                ads.append(img_path)
        return ads
    
    # Streamlit Code to Display Customer Data
    st.title("Personalized Ads - Lazana")
    
    # Path to the downloaded CSV file (update this path based on where your CSV is saved)
    file_path = "purchase_history.csv"
    
    # Load the data
    customer_data_df = load_customer_data(file_path)
    
    # Convert customer data into a more useful format for analysis
    customer_data = {}
    for _, row in customer_data_df.iterrows():
        customer_name = row['customer_name']
        purchases = [row['product_category1'], row['product_category2'], row['product_category3'], row['product_name']]
        customer_data[customer_name] = purchases
    
    # Customer Selection
    selected_customer = st.selectbox("Select a Customer", customer_data.keys())
    
    if selected_customer:
        # Step 1: Analyze customer data
        customer_analysis = customer_analyst(selected_customer)
        st.write(customer_analysis)
    
        # Step 2: Analyze purchases
        purchases = customer_data.get(selected_customer, [])
        purchase_analysis = purchase_analyzer(selected_customer, purchases)
        st.write(purchase_analysis)
    
        # Step 3: Classify purchases into categories
        categories = category_classifier(purchases)
        st.write(f"Classified Categories: {', '.join(categories)}")
    
        # Step 4: Orchestrator selects ads based on classification
        ads = orchestrator(selected_customer, categories)
        for ad in ads:
            st.image(ad, caption=f"Personalized Ad for {selected_customer}", use_column_width=True)
