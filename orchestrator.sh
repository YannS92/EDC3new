#!/bin/bash

viewports=("desktop" "mobile" "tablet")

for viewport in "${viewports[@]}"; do
    echo "▶ Running $viewport"
    docker compose run --rm tests tests/ -v --headless -n auto --viewport=$viewport --reruns 1 --reruns-delay 2 --html=reports/report-$viewport.html --self-contained-html
done
