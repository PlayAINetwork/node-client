# Dockerfile
# Start from a base Ubuntu image
FROM ubuntu:latest
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy the Python scripts and requirements.txt into the container
COPY pull-service.py /app/pull-service.py
#COPY process.py /app/process.py
#COPY main_server.py /app/main_server.py
COPY my_wrapper_script.sh /app/my_wrapper_script.sh
COPY requirements.txt /app/requirements.txt
COPY .env /app/.env
COPY app.py /app/app.py

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x /app/my_wrapper_script.sh


# Command to run the Flask app (file2.py)
CMD ["/app/my_wrapper_script.sh"]

EXPOSE 3000
