import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

project_name = "ai_ecommerce_assistant"

list_of_files = [
    ".github/workflows/.gitkeep",
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/components/chatbot.py",                # Chatbot logic
    f"src/{project_name}/components/recommendation.py",         # Recommendation system logic
    f"src/{project_name}/components/negotiation.py",            # Negotiation strategies logic
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/utils/common.py",                      # Common utility functions
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/config/configuration.py",              # Configuration management
    f"src/{project_name}/pipeline/__init__.py",
    f"src/{project_name}/pipeline/model_pipeline.py",           # Model training and inference pipeline
    f"src/{project_name}/entity/__init__.py",
    f"src/{project_name}/entity/config_entity.py",              # Configuration entities
    f"src/{project_name}/constants/__init__.py",                # Constant variables
    f"src/{project_name}/constants/constants.py",
    "config/config.yaml",                                       # Configuration file
    "params.yaml",                                              # Parameters for model and pipeline
    "schema.yaml",                                              # Schema definitions for data validation
    "main.py",                                                  # Main entry point for running the app
    "app.py",                                                   # Flask app entry point
    "Dockerfile",                                               # Docker setup
    "requirements.txt",                                         # Project dependencies
    "setup.py",                                                 # Package setup
    "research/trials.ipynb",                                    # Research and experimentation notebook
    "templates/index.html",                                     # HTML template for frontend
    "static/css/styles.css",                                    # CSS for frontend
    "static/js/scripts.js",                                     # JavaScript for frontend
    "data/training_data.csv",                                   # Dataset for training
    "data/product_data.csv",                                    # Product dataset
    "models/.gitkeep"                                           # Model directory placeholder
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for the file: {filename}")

    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        with open(filepath, "w") as f:
            pass
        logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filename} already exists")
