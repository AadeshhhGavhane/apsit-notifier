FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot code
COPY bot.py .

# Create data directory
RUN mkdir -p data

CMD ["python", "bot.py"]