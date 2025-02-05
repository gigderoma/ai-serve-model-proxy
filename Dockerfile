FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Expose the port your Flask app listens on.  Important for OpenShift!
EXPOSE 5000

# Set environment variables for Flask (optional, but good practice)
ENV FLASK_APP app.py  # Replace app.py with your main Flask file if different
ENV FLASK_ENV production # Or development if needed

# For running on OpenShift, bind to all interfaces (0.0.0.0)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--threads", "4", "app:app"] # Use gunicorn for production. Adjust workers/threads as needed.
