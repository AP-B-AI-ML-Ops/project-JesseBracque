FROM python:3.13-slim

RUN pip install -U pip

# Set the working directory inside the container
WORKDIR /app

# Copy everything needed into the container
COPY requirements.txt ./
COPY startPoolWorkers.sh ./
COPY scripts ./scripts
COPY data-files ./data

RUN pip install -r requirements.txt --upgrade

RUN chmod +x ./startPoolWorkers.sh

# Set environment variable for Prefect (this is better than using RUN)
ENV PREFECT_API_URL="http://orchestration:4200/api"

# Run the startup script using exec form (recommended)
CMD ["/bin/bash", "startPoolWorkers.sh"]