# Cron Jobs

Two Hermes Agent cron jobs automate the daily diesel data pipeline.

## Daily collection — 02:00 MSK

- Runs `diesel-heatmap-daily` job (`c20d0ade1f2f`)
- Scrapes fresh restriction data from regional sources
- Updates the heatmap data and regenerates `data.json`
- Writes output to `/srv/static/` (served by Caddy at cockpit.borovikvv.ru/static/)

## Daily publish — 11:00 MSK

- Runs `publish-diesel-daily` job (`5792c3b0a0b0`)
- Generates a human-readable summary of daily changes
- Publishes the changelog to Telegram channel @disel_limits_update
- Source: `/root/diesel_limits/` git repo
- Web root: `/srv/static/`
