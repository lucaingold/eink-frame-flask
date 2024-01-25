# syntax=docker/dockerfile:1

FROM python:alpine3.19

WORKDIR /app

COPY requirements.txt .

# Install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the entire application
COPY controller controller
COPY src src
COPY static static
COPY templates templates
COPY app.py .

# Expose the necessary ports
EXPOSE 5000
EXPOSE 1883
EXPOSE 8883

# Start the Flask application
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]