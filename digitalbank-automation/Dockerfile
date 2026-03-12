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
    PYTEST_MARKERS="" \
    REPORT_DIR=reports

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT [\
  "sh", "-c", "\
  MARKERS_ARG=\"\"; \
  if [ -n \"${PYTEST_TAGS}\" ]; then \
    MARKERS_ARG=\"-m ${PYTEST_TAGS}\"; \
  fi; \
  CMD=\"pytest tests/ -v \
    -n ${PARALLEL_PROCESSES} \
    --reruns ${RERUN_NB} \
    --reruns-delay ${RERUN_DELAY} \
    --env ${ENV} \
    --browser ${BROWSER} \
    --viewport ${VIEWPORT} \
    --alluredir ${REPORT_DIR}/allure-results \
    ${MARKERS_ARG} \
    --html ${REPORT_DIR}/report-${BROWSER}-${VIEWPORT}.html \
    --self-contained-html\"; \
  echo \"Running: ${CMD}\"; \
  eval \"${CMD}\"\
  "\
]
