FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY slack_verification_requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY slack_verification.py app.py

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
