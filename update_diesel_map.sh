#!/bin/bash
set -e
cd /root/ai_business_pulse_hermes
python3 tmp/gen_diesel_map.py
cp /root/ai_business_pulse_hermes/tmp/diesel_heatmap_20260703.png /srv/static/diesel.png
echo "Diesel heatmap updated and deployed"
