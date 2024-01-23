# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .

# Install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the entire application
COPY . .

# Expose the necessary ports
EXPOSE 5000
EXPOSE 1883

# Start the Flask application
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]