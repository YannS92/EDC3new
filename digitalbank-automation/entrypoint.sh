#!/bin/bash
# Entrypoint des conteneurs de test DigitalBank
# Les variables sont lues depuis l'environnement du conteneur (docker-compose environment:)

exec pytest tests/ -v \
  -n "${PARALLEL_PROCESSES:-auto}" \
  --reruns "${RERUN_NB:-1}" \
  --reruns-delay "${RERUN_DELAY:-2}" \
  --env "${ENV:-dev}" \
  --browser "${BROWSER:-chromium}" \
  --viewport "${VIEWPORT:-desktop}" \
  --alluredir "${REPORT_DIR:-reports}/allure-results" \
  --html "${REPORT_DIR:-reports}/report-${BROWSER:-chromium}-${VIEWPORT:-desktop}.html" \
  --self-contained-html \
  "$@"
