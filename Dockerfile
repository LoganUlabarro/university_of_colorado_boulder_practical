# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN apt-get update && \
    apt-get install -y gcc build-essential wget unzip curl unixodbc-dev libnss3 libgconf-2-4 libxi6 libgdk-pixbuf2.0-0 libxcomposite1 libxrandr2 libxss1 libxtst6 libappindicator1 fonts-liberation xdg-utils libgbm1 && \
    rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] https://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get update && apt-get install -y google-chrome-stable

# Install ChromeDriver
RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    wget -N https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    rm chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver

# Install Python packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set environment variable
ENV PYTHONPATH "${PYTHONPATH}:/app"

# Run pytest command
CMD ["pytest", "-s", "-v", "testFiles/google_demo.py"]
