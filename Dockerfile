# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and application code to the container
COPY requirements.txt .
COPY streamlit_gitlab_review.py .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit's default port
EXPOSE 8501


docker build -t streamlit-gitlab-review .
docker run -p 8501:8501 streamlit-gitlab-review
streamlit
requests
openai


# Run the Streamlit app
CMD ["streamlit", "run", "streamlit_gitlab_review.py", "--server.port=8501", "--server.enableCORS=false"]
