import streamlit as st
import pandas as pd

# Title
st.title("Generate Image URLs for Items in a CSV File")

# File uploader
uploaded_file = st.file_uploader("Upload a CSV file with items", type="csv")

if uploaded_file is not None:
    # Read the CSV file
    df = pd.read_csv(uploaded_file)
    st.write("Uploaded CSV File:", df)
    
    # Check for a specific column (e.g., "Item")
    if "Item" in df.columns:
        items = df["Item"]
        
        # Mock image URLs (replace with API logic for real images)
        base_url = "https://via.placeholder.com/150?text="
        df["Image URL"] = items.apply(lambda x: f"{base_url}{x.replace(' ', '+')}")
        
        # Display the updated DataFrame
        st.write("Updated CSV File with Image URLs:", df)
        
        # Optionally download the updated CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Updated CSV",
            data=csv,
            file_name="updated_image_urls.csv",
            mime="text/csv",
        )
    else:
        st.error("The uploaded CSV must contain a column named 'Item'.")
