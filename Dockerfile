# Use a more secure and stable base image
FROM python:3.10-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends gcc curl build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy your code into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose port expected by Hugging Face Spaces (or keep default 7860)
EXPOSE 7860

# Command to run your Dash app
CMD ["python", "app.py"]
