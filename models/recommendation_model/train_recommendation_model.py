import pandas as pd
from transformers import BertTokenizer, BertModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm
import os

# Load the dataset
data = pd.read_csv('./data/enhanced_dataset_with_synthetic_negotiations.csv')

# Prepare the BERT model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
bert_model = BertModel.from_pretrained('bert-base-uncased')

# Define the directory to save the model and tokenizer
save_directory = './saved_bert_model/'

# Create the directory if it doesn't exist
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

# Save the tokenizer and model
tokenizer.save_pretrained(save_directory)
bert_model.save_pretrained(save_directory)

print(f"Model and tokenizer saved to {save_directory}")

# Function to get BERT embeddings for text
def get_bert_embedding(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
    with torch.no_grad():
        outputs = bert_model(**inputs)
    return outputs.last_hidden_state.mean(dim=1)

# Compute BERT embeddings for the 'clean_description' column
print("Starting embedding computation...")
tqdm.pandas()
data['bert_embedding'] = data['clean_description'].progress_apply(lambda x: get_bert_embedding(x).cpu().numpy().flatten())
print("Embeddings computed successfully!")

# Compute the cosine similarity matrix for the embeddings
embeddings = torch.tensor(data['bert_embedding'].tolist())  # Convert to tensor for cosine similarity
cosine_sim = cosine_similarity(embeddings)

# Function to recommend products based on cosine similarity
def recommend_products(item_id, top_n=5):
    # Get the similarity scores for the selected item (item_id)
    item_index = data[data['uniq_id'] == item_id].index[0]
    similarity_scores = cosine_sim[item_index]

    # Create a DataFrame for the similarity scores with corresponding 'main_category', 'product_name', and 'recommend_to_others' values
    similarity_df = pd.DataFrame({
        'item_id': data['uniq_id'],
        'similarity_score': similarity_scores,
        'recommend_to_others': data['recommend_to_others'],  # Include 'recommend_to_others'
        'main_category': data['main_category'],  # Add 'main_category'
        'product_name': data['product_name']    # Add 'product_name'
    })

    # Sort by cosine similarity in descending order and include 'recommend_to_others'
    similarity_df = similarity_df.sort_values(by=['recommend_to_others', 'similarity_score'], ascending=[False, False])

    # Get the top N most similar items (excluding the item itself)
    top_recommendations = similarity_df[similarity_df['item_id'] != item_id].head(top_n)

    # Format the output as required, excluding 'recommend_to_others' from the output
    top_recommendations = top_recommendations[['item_id', 'main_category', 'product_name']]

    return top_recommendations

# Example: Get recommendations for an item (replace with an actual item_id)
item_id = 'e54bc0a7c3429da2ebef0b30331fe3d2'  # Sample item_id from your dataset
recommendations = recommend_products(item_id)

# Display the recommendations in the desired format
print(f"Recommendations for item: {item_id}")
for _, row in recommendations.iterrows():
    print(f"{row['item_id']} || {row['main_category']} | {row['product_name']}")
