FROM python:3.13-slim

RUN pip install -U pip

# Set the working directory inside the container
WORKDIR /app

# Copy everything needed into the container
COPY requirements.txt ./

RUN pip install -r requirements.txt --upgrade

COPY . .
RUN chmod +x ./startPoolWorkersAndDeployments.sh

# Set environment variable for Prefect (this is better than using RUN)
ENV PREFECT_API_URL="http://orchestration:4200/api"

# Run the startup script using exec form (recommended)
CMD ["bash", "startPoolWorkersAndDeployments.sh"]