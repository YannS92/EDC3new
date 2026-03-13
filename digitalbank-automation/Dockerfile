# Dockerfile - DigitalBank Tests
# ─────────────────────────────────────────────────────────────────────
# Image de base : mcr.microsoft.com/playwright/python (Chromium/Firefox/WebKit inclus)
#
# Variables d'environnement configurables au runtime via docker-compose :
#   BROWSER            : navigateur cible (chromium | firefox | webkit)
#   VIEWPORT           : résolution (desktop | mobile | tablet)
#   ENV                : environnement pytest (dev | docker | uat ...)
#   PARALLEL_PROCESSES : workers pytest-xdist (auto | 1 | N)
#   PYTEST_MARKERS     : filtre marqueur pytest (smoke | regression | ...)
#   RERUN_NB           : relances sur test flaky
#   RERUN_DELAY        : délai (s) entre relances
#   REPORT_DIR         : dossier de sortie des rapports
#
# L'ENTRYPOINT construit dynamiquement la commande pytest en fonction
# des variables d'environnement, puis l'évalue via eval.
# ─────────────────────────────────────────────────────────────────────

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
  if [ -n \"${PYTEST_MARKERS}\" ]; then \
    MARKERS_ARG=\"-m ${PYTEST_MARKERS}\"; \
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
