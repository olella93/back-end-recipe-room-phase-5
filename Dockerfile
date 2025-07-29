# Use official Python image
FROM python:3.8-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port
EXPOSE 5000

# Run the app
CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]
