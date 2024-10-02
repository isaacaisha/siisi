# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install necessary system dependencies, including Chromium and Chromedriver
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    unzip \
    curl \
    libnss3 \
    libxss1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libgtk-4-1 \
    libu2f-udev \
    libvulkan1 \
    libxkbcommon0 \
    ffmpeg \
    chromium \
    chromium-driver \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for Chromium
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_BIN=/usr/bin/chromedriver

# Copy the requirements file into the container
COPY requirements.txt /app/requirements.txt

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Set environment variables (if needed)
ENV PORT=8000

# Expose port 8000 (default for Django)
EXPOSE 8000

# Collect static files (uncomment if needed in production)
RUN python manage.py collectstatic --noinput

# Add a health check to verify if the app is running
HEALTHCHECK CMD curl --fail http://localhost:8000 || exit 1

# Use Gunicorn with Uvicorn worker to run the Django ASGI app
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "siisi.asgi:application", "--bind", "0.0.0.0:8000"]
