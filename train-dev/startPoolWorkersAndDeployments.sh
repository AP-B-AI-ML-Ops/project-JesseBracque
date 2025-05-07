#!/bin/bash

# To make sure thie script is executed when the prefect server is started
sleep 30

prefect config set PREFECT_API_URL="http://localhost:4200/api"

prefect work-pool create --type process main --overwrite
prefect worker start -p main &

python ./deployments/training_deployment.py &
python ./deployments/registration_deployment.py