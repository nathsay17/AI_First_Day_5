import os
import openai
import pandas as pd
import streamlit as st
import warnings
from streamlit_option_menu import option_menu
from streamlit_extras.mention import mention
from strings import home_string, System_Prompt

warnings.filterwarnings("ignore")
st.set_page_config(page_title="Lazana", page_icon="🤖", layout="wide")

# Load the CSV file with customer product data
def load_csv():
    file_path = "customer_recommendations.csv"  # Path to your CSV file in the repo
    df = pd.read_csv(file_path)
    return df

# Function to display images for the selected customer's products
def display_images_for_customer(customer_name, df):
    # Find the customer row based on their name
    customer_data = df[df['name'] == customer_name]
    
    if not customer_data.empty:
        # Get the products for the customer
        products = customer_data.iloc[0, 1:].values  # Get product1 to product4
        
        # Loop through the products and display images
        for product in products:
            if product != 'N/A':  # Skip 'N/A' values
                image_path = os.path.join("images", f"{product}.png")  # Adjust extension if needed
                if os.path.exists(image_path):  # Ensure the image file exists
                    st.image(image_path, caption=product, use_column_width=True)
                else:
                    st.warning(f"Image for {product} not found.")
    else:
        st.warning(f"No data found for {customer_name}.")

# Display buttons for each customer and show corresponding product images
def display_customer_buttons():
    # Load the customer recommendations CSV file
    df = load_csv()

    # Buttons for each customer
    customers = ["Xyrel", "Carlo", "Amber", "Danielle"]
    
    # Display button for each customer
    for customer in customers:
        if st.button(customer):
            display_images_for_customer(customer, df)

# Main content based on sidebar selection
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_session" not in st.session_state:
    st.session_state.chat_session = None  # Placeholder for your chat session initialization

st.set_page_config(page_title="Lazana", page_icon="🤖", layout="wide")

with st.sidebar:
    st.image('images/Lazana1.png')
    
    openai.api_key = st.text_input('Enter OpenAI API token:', type='password')
    if not (openai.api_key.startswith('sk-') and len(openai.api_key) == 164):
        st.warning('Please enter your OpenAI API token!', icon='⚠️')
    else:
        st.success('Proceed to entering your prompt message!', icon='👉')

    with st.container():
        l, m, r = st.columns((1, 3, 1))
        with l:
            st.empty()
        with m:
            st.empty()
        with r:
            st.empty()

    options = option_menu(
        "Content",
        ["Home", "Data Set"],
        icons=['heart', 'clipboard'],
        menu_icon="book",
        default_index=0,
        styles={
            "icon": {"color": "#ffffff", "font-size": "20px"},
            "nav-link": {"font-size": "17px", "text-align": "left", "margin": "5px", "--hover-color": "#354373"},
            "nav-link-selected": {"background-color": "#1b8cc4"}
        }
    )

if options == "Home":
    st.markdown(home_string, unsafe_allow_html=True)

elif options == "Data Set":
    st.title("Customer Recommendations")

    # Display buttons for each customer
    display_customer_buttons()
