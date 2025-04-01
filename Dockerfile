FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# No need to copy Python files as they'll be mounted
# The .env file will also be mounted

# Set the working directory to where the code will be mounted
WORKDIR /app/src

# Run the bot
CMD ["python", "bot.py"] 