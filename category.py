import openai
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Set up your OpenAI API key
openai.api_key = ''

# Predefined categories
categories = [
    "cat_bed", "cat_collar", "cat_food", "cat_toy",
    "dog_bed", "dog_food", "dog_leash", "dog_toy",
    "shoes_boots", "shoes_heels", "shoes_sneakers", "shoes_wedge",
    "watch_electronic", "watch_premium", "watch_regular"
]

# Function to get embeddings
def get_openai_embedding(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return np.array(response['data'][0]['embedding'])

# Load the dataset
dataset_url = 'https://docs.google.com/spreadsheets/d/1xV_kym5oqxD_1fsA7YzzKgsV-N29d-Q1dHBoDa6PtvI/export?format=csv&gid=0'
df = pd.read_csv(dataset_url)

# Combine columns into a single string for embedding input
df['combined_text'] = df.apply(
    lambda row: ' '.join([str(row['product_category1']), str(row['product_category2']), str(row['product_category3']), str(row['product_name'])]),
    axis=1
)

# Get embeddings for all combined text
df['embedding'] = df['combined_text'].apply(get_openai_embedding)

# Get embeddings for category labels
category_embeddings = {cat: get_openai_embedding(cat) for cat in categories}

# Assign the closest category based on cosine similarity
def assign_category(row_embedding):
    similarities = {cat: cosine_similarity([row_embedding], [cat_embedding])[0][0]
                    for cat, cat_embedding in category_embeddings.items()}
    return max(similarities, key=similarities.get)

df['customer_category'] = df['embedding'].apply(assign_category)

# Drop the embedding column as it's not needed further
df = df.drop(columns=['embedding'])

# The updated dataframe is ready for further analysis
print(df.head())
