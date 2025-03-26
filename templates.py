import os
import logging

# Configure logging
logging.basicConfig(
    filename="project_creation.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Define the project structure
project_structure = {
    "ecommerce_project": {
        "data": {
            "enhanced_dataset_with_synthetic_negotiations.csv": "",
            "README.md": "Dataset description goes here.",
        },
        "models": {
            "negotiation_model": {
                "trained_model": {},
                "train_negotiation_model.py": "# Training script for negotiation model",
                "README.md": "Documentation for the negotiation model.",
            },
            "recommendation_model": {
                "train_recommendation_model.py": "# Training script for recommendation system",
                "README.md": "Documentation for the recommendation model.",
            },
        },
        "src": {
            "__init__.py": "# Init file for the 'src' directory",
            "negotiation.py": "# Functions for handling negotiation system",
            "recommendation.py": "# Functions for handling recommendation system",
            "utils.py": "# Utility functions (e.g., tokenization, data processing)",
            "config.py": "# Configuration file (hyperparameters, model paths, etc.)",
        },
        "requirements.txt": "# Project dependencies",
        "run_negotiation.py": "# Script to run the fine-tuned negotiation model",
        "run_recommendation.py": "# Script to run the recommendation system",
        "train.py": "# Main training script for both systems",
        "logs": {},  # Logs folder
        "README.md": "Project overview and setup instructions",
    }
}

def create_structure(base_path, structure):
    """
    Recursively create directories and files based on the provided structure.
    :param base_path: The base directory path.
    :param structure: The directory structure as a nested dictionary.
    """
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            # Create directory
            try:
                os.makedirs(path, exist_ok=True)
                logging.info(f"Created directory: {path}")
            except Exception as e:
                logging.error(f"Failed to create directory {path}: {e}")

            # Recursively create subdirectories/files
            create_structure(path, content)
        else:
            # Create file with initial content
            try:
                with open(path, "w") as file:
                    file.write(content)
                logging.info(f"Created file: {path}")
            except Exception as e:
                logging.error(f"Failed to create file {path}: {e}")

if __name__ == "__main__":
    # Base directory for the project
    base_dir = os.getcwd()  # Current working directory
    project_name = "ecommerce_project"
    project_path = os.path.join(base_dir, project_name)

    # Create the project structure
    try:
        create_structure(base_dir, project_structure)
        logging.info(f"Project structure for '{project_name}' has been created at {project_path}")
        print(f"Project structure for '{project_name}' has been created at {project_path}")
    except Exception as e:
        logging.critical(f"Failed to create project structure: {e}")
        print(f"Failed to create project structure: {e}")
