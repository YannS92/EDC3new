# Dockerfile - DigitalBank Tests
# Playwright vient avec Chromium / Webkit / Firefox

FROM mcr.microsoft.com/playwright/python:v1.42.0-jammy

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["pytest"]
