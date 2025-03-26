# Import necessary libraries
import os
import pandas as pd
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    Trainer,
    TrainingArguments
)

# Disable WandB logging
os.environ["WANDB_DISABLED"] = "true"

# Step 1: Load the dataset
file_path = './data/enhanced_dataset_with_synthetic_negotiations.csv'  # Update with your dataset path
data = pd.read_csv(file_path)

# Extract the negotiation dialogue column and drop missing values
dialogue_data = data[['negotiation_dialogue']].dropna()

# Convert to Hugging Face Dataset format
dialogue_dataset = Dataset.from_pandas(dialogue_data)

# Step 2: Load DialoGPT-medium tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")

# Add padding token if not present
if tokenizer.pad_token is None:
    tokenizer.add_special_tokens({'pad_token': tokenizer.eos_token})

model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
model.resize_token_embeddings(len(tokenizer))  # Resize embeddings after adding padding token

# Step 3: Tokenization function
def tokenize_function(example):
    tokenized_output = tokenizer(
        example['negotiation_dialogue'],
        truncation=True,
        padding="max_length",
        max_length=512
    )
    tokenized_output["labels"] = tokenized_output["input_ids"].copy()
    return tokenized_output

# Apply tokenization
tokenized_dataset = dialogue_dataset.map(tokenize_function, batched=True)

# Step 4: Split into train and validation sets
train_test_split = tokenized_dataset.train_test_split(test_size=0.1)
train_dataset = train_test_split["train"]
val_dataset = train_test_split["test"]

# Convert dataset into PyTorch format
train_dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "labels"])
val_dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "labels"])

# Step 5: Define training arguments with acceleration
training_args = TrainingArguments(
    output_dir="./results",  # Directory to save model checkpoints
    evaluation_strategy="epoch",  # Evaluate after each epoch
    learning_rate=5e-5,  # Learning rate
    per_device_train_batch_size=1,  # Per-device batch size
    per_device_eval_batch_size=1,  # Per-device evaluation batch size
    gradient_accumulation_steps=8,  # Simulate larger batch size
    num_train_epochs=3,  # Number of training epochs
    weight_decay=0.01,  # Weight decay
    save_total_limit=2,  # Limit number of checkpoints
    logging_dir="./logs",  # Directory for logs
    logging_steps=10,  # Log every 10 steps
    fp16=True,  # Enable mixed precision
    push_to_hub=False,  # Disable pushing to Hugging Face Hub
)

# Step 6: Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
)

# Step 7: Train the model
trainer.train()

# Step 8: Save the model
model_dir = "./newtrained_model"
if not os.path.exists(model_dir):
    os.makedirs(model_dir)

model.save_pretrained(model_dir)
tokenizer.save_pretrained(model_dir)

print("Model and tokenizer saved to:", model_dir)
