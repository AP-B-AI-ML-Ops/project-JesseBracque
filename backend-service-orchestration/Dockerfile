FROM python:3.11-slim

RUN pip install -U pip setuptools wheel

WORKDIR /prefect

COPY ["./.prefectignore", "./prefect.yaml", "./"]

RUN pip install pendulum prefect --upgrade

# Set the Prefect API URL to the service name
RUN prefect config set PREFECT_API_URL="http://orchestration:4200/api"

# Expose the port
EXPOSE 4200

# Start the Prefect server
CMD ["prefect", "server", "start", "--host", "0.0.0.0", "--port", "4200"]

# Make worker
# CMD ["prefect", "work-pool", "--type", "process", "work-pool-1", "--overwrite"]