# Dockerfile
# Start from a base Ubuntu image
FROM ubuntu:latest
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


RUN chmod +x my_wrapper_script.sh


# Command to run the Flask app (file2.py)
CMD ["/app/my_wrapper_script.sh"]

EXPOSE 3000
