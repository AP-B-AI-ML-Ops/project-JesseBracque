#!/bin/bash

sleep 40

prefect work-pool create --type process batch --overwrite
prefect worker start -p batch &

python /app/batch.py &
python /app/import_daily_to_db.py