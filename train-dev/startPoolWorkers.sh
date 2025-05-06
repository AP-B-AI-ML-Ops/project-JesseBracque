#!/bin/bash
prefect config set PREFECT_API_URL="http://orchestration:4200/api"

prefect work-pool create --type process main --overwrite
prefect worker start -p main &

# python ./scripts/main.py