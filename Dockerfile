FROM python:3.10-slim-buster

WORKDIR /app

COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 8080

# Run the Flask app
CMD ["python3", "app.py"]
