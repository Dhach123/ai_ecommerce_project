from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
import os
import pandas as pd
import numpy as np
from transformers import AutoTokenizer, AutoModelForCausalLM, BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)  # Allow requests from React frontend

# Define paths dynamically
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NEGOTIATION_MODEL_PATH = os.path.join(BASE_DIR, "newtrained_model")
RECOMMENDATION_MODEL_PATH = os.path.join(BASE_DIR, "saved_bert_model")
DATASET_PATH = os.path.join(BASE_DIR, "data", "enhanced_dataset_with_synthetic_negotiations.csv")
EMBEDDINGS_PATH = os.path.join(BASE_DIR, "data", "bert_embeddings.npy")

# ✅ Load negotiation model
negotiation_tokenizer = AutoTokenizer.from_pretrained(NEGOTIATION_MODEL_PATH)
negotiation_model = AutoModelForCausalLM.from_pretrained(NEGOTIATION_MODEL_PATH)

# ✅ Load BERT model for recommendations
bert_tokenizer = BertTokenizer.from_pretrained(RECOMMENDATION_MODEL_PATH)
bert_model = BertModel.from_pretrained(RECOMMENDATION_MODEL_PATH)

# ✅ Load dataset
data = pd.read_csv(DATASET_PATH)

# ✅ Load precomputed BERT embeddings
if os.path.exists(EMBEDDINGS_PATH):
    embeddings = np.load(EMBEDDINGS_PATH)
else:
    embeddings = None  # Prevent crashes
    print("❌ Embeddings file not found. Run the embedding generation script.")

# 🏠 **Home Route**
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Recommendation API! Use /chat or /recommendations?item_id=<ID>"}), 200

# 🛒 **NEGOTIATION CHATBOT ENDPOINT**
@app.route('/chat', methods=['GET'])
def chat():
    user_message = request.args.get('message', '').strip()
    
    if not user_message:
        return jsonify({"error": "Message cannot be empty"}), 400

    # Context for negotiation
    context = "Customer wants a discount. Salesperson is negotiating."
    prompt = f"{context}\nCustomer: {user_message}\nSalesperson:"

    inputs = negotiation_tokenizer(prompt, return_tensors="pt")
    outputs = negotiation_model.generate(
        inputs["input_ids"],
        max_new_tokens=50,
        num_beams=5,
        temperature=0.8,
        top_p=0.95,
        do_sample=True,
        pad_token_id=negotiation_tokenizer.eos_token_id
    )

    response = negotiation_tokenizer.decode(outputs[0], skip_special_tokens=True)
    response_text = response.split("Salesperson:")[-1].strip()

    return jsonify({"response": response_text})

# 🔥 **PRODUCT RECOMMENDATION ENDPOINT**
@app.route('/recommendations', methods=['GET', 'POST'])
def recommend():
    if request.method == 'POST':
        data_req = request.get_json()
        item_id = data_req.get('item_id', '').strip()
    else:
        item_id = request.args.get('item_id', '').strip()

    if not item_id or item_id not in data['uniq_id'].values:
        return jsonify({"error": "Invalid or missing item_id"}), 400

    if embeddings is None:
        return jsonify({"error": "Embeddings not loaded. Please generate and load embeddings first."}), 500

    # Get index of item
    item_index = data[data['uniq_id'] == item_id].index[0]
    similarity_scores = cosine_similarity([embeddings[item_index]], embeddings)[0]

    # Create DataFrame with similarity scores
    similarity_df = pd.DataFrame({
        'item_id': data['uniq_id'],
        'similarity_score': similarity_scores,
        'recommend_to_others': data['recommend_to_others'],
        'main_category': data['main_category'],
        'product_name': data['product_name']
    })

    # Sort by recommendation score
    similarity_df = similarity_df.sort_values(by=['recommend_to_others', 'similarity_score'], ascending=[False, False])

    # Exclude the queried item itself
    top_recommendations = similarity_df[similarity_df['item_id'] != item_id].head(5)

    return jsonify(top_recommendations[['item_id', 'main_category', 'product_name']].to_dict(orient="records"))

# ✅ **RUN FLASK SERVER (Port 8000)**
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
