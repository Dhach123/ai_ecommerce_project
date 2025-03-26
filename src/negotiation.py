from transformers import AutoTokenizer, AutoModelForCausalLM

# Load the fine-tuned model and tokenizer
model_path = "./newtrained_model"  # Update if necessary
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)

# Ensure tokenizer has a padding token
if tokenizer.pad_token is None:
    tokenizer.add_special_tokens({'pad_token': tokenizer.eos_token})
    model.resize_token_embeddings(len(tokenizer))

# User input for negotiation
input_text = "give me discount"

# Context for negotiation
context = """
Customer is asking for a discount. The salesperson is negotiating a price.
"""

# Combine context with the customer input to guide the model's response
prompt = f"{context}\nCustomer: {input_text}\nSalesperson:"

# Encode the combined input for model generation
inputs = tokenizer(prompt.strip(), return_tensors="pt")

# Generate response with improved negotiation-focused parameters
outputs = model.generate(
    inputs["input_ids"],
    attention_mask=inputs["attention_mask"],
    max_new_tokens=50,  # Controls new token length
    num_beams=5,  # Beam search with more beams to find better response
    temperature=0.8,  # Moderate randomness
    top_p=0.95,  # Increased to allow more creative responses
    top_k=50,  # Top-K sampling
    do_sample=True,  # Enable sampling for varied responses
    pad_token_id=tokenizer.eos_token_id,
    length_penalty=1.5,  # Encourages longer responses
    early_stopping=True
)

# Decode the generated output
generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

# Clean up the response by removing unwanted parts of the context
response = generated_text.split("Salesperson:")[-1].strip()

# Print final response
print("AI Response:", response)
