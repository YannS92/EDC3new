# Dockerfile - DigitalBank Tests
# Playwright vient avec Chromium / Webkit / Firefox

FROM mcr.microsoft.com/playwright/python:v1.42.0-jammy

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PARALLEL_PROCESSES=1 \
    RERUN_NB=1 \
    RERUN_DELAY=2 \
    ENV=dev \
    BROWSER=chromium \
    VIEWPORT=desktop \
    REPORT_DIR=reports

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT [ \
    "sh", "-c", \
    "pytest tests/ -v \
    -n ${PARALLEL_PROCESSES} \
    --reruns ${RERUN_NB} \
    --reruns-delay ${RERUN_DELAY} \
    --env ${ENV} \
    --browser ${BROWSER} \
    --viewport ${VIEWPORT} \
    --alluredir ${REPORT_DIR}/allure-results \
    --html ${REPORT_DIR}/report-${BROWSER}-${VIEWPORT}.html \
    --self-contained-html" \
]
