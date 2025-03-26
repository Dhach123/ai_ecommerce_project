from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os
from transformers import BertTokenizer, BertModel

app = Flask(__name__)
CORS(app)

# Load dataset and precomputed embeddings
data_file = './data/enhanced_dataset_with_synthetic_negotiations.csv'
embedding_file = './data/bert_embeddings.npy'
data = pd.read_csv(data_file)
save_directory = './saved_bert_model/'

tokenizer = BertTokenizer.from_pretrained(save_directory)
bert_model = BertModel.from_pretrained(save_directory)

if os.path.exists(embedding_file):
    embeddings = np.load(embedding_file)
else:
    raise FileNotFoundError("BERT embeddings not found!")

cosine_sim = cosine_similarity(embeddings)

@app.route('/get_unique_ids', methods=['GET'])
def get_unique_ids():
    unique_ids = data['uniq_id'].tolist()
    return jsonify({'unique_ids': unique_ids})

@app.route('/recommend', methods=['POST'])
def recommend():
    content = request.get_json()
    item_id = content.get('item_id')

    if not item_id or item_id not in data['uniq_id'].values:
        return jsonify({'error': 'Invalid or missing item_id'}), 400

    try:
        item_index = data[data['uniq_id'] == item_id].index[0]
        similarity_scores = cosine_sim[item_index]

        similarity_df = pd.DataFrame({
            'item_id': data['uniq_id'],
            'similarity_score': similarity_scores,
            'recommend_to_others': data['recommend_to_others'],
            'main_category': data['main_category'],
            'product_name': data['product_name']
        })

        similarity_df = similarity_df.sort_values(
            by=['recommend_to_others', 'similarity_score'],
            ascending=[False, False]
        )

        top_recommendations = similarity_df[similarity_df['item_id'] != item_id].head(5)
        recommendations = top_recommendations.to_dict(orient='records')

        return jsonify({'recommendations': recommendations})

    except Exception as e:
        print(f"Recommendation error: {e}")
        return jsonify({'error': 'Server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
