import requests
import pandas as pd
import streamlit as st

# Unsplash API credentials
UNSPLASH_ACCESS_KEY = "ChAMp9kD1hwKEiGQiU6blJ41y6kZuIzIyxs1TaU81Kk"  # Replace with your actual API key

# Function to search for an image
def get_image_url(query):
    url = f"https://api.unsplash.com/search/photos"
    params = {"query": query, "client_id": UNSPLASH_ACCESS_KEY, "per_page": 1}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["results"]:
            return data["results"][0]["urls"]["regular"]
        else:
            return "No image found"
    else:
        return "API error"

# Streamlit app
st.title("Fetch Real Image URLs for Items")

# File uploader
uploaded_file = st.file_uploader("Upload a CSV file with an 'Item' column", type="csv")
if uploaded_file is not None:
    # Read the CSV file
    df = pd.read_csv(uploaded_file)
    if "Item" in df.columns:
        # Add image URLs
        df["Image URL"] = df["Item"].apply(get_image_url)
        st.write("Updated CSV with Image URLs:", df)

        # Allow download of the updated file
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Updated CSV",
            data=csv,
            file_name="updated_image_urls.csv",
            mime="text/csv",
        )
    else:
        st.error("The uploaded file must contain an 'Item' column.")
