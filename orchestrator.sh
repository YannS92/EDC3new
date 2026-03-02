#!/bin/bash

browsers=("chrome" "firefox")
viewports=("desktop" "mobile" "tablet")

for viewport in "${viewports[@]}"; do
    echo "▶ Running $viewport"
    VIEWPORT=$viewport docker compose run --rm tests
done