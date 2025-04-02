# Use an official Python runtime as base image
FROM python:3.8

# Set the working directory
WORKDIR /app

# Copy the project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask port
EXPOSE 8000

# Run the application
CMD ["python", "app.py"]
