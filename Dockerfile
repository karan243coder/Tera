# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file (if you have one) and the bot script into the container
COPY requirements.txt ./
COPY terabox_bot.py ./

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the bot
CMD gunicorn app:app & python3 main.py