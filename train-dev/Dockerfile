FROM python:3.13-slim

RUN pip install -U pip

# Set the working directory inside the container
WORKDIR /app

# Copy everything needed into the container
COPY . .

RUN pip install -r requirements.txt --upgrade

RUN chmod +x ./startPoolWorkersAndDeployments.sh

# Set environment variable for Prefect (this is better than using RUN)
ENV PREFECT_API_URL="http://orchestration:4200/api"

# Create deployments during container build
#RUN prefect deploy deployments/training_deployment.py:training_pipeline \
#    && prefect deploy deployments/registration_deployment.py:registration_pipeline

# Run the startup script using exec form (recommended)
CMD ["bash", "startPoolWorkersAndDeployments.sh"] 

# "sh", "-c", "prefect deploy deployments/training_deployment.py && prefect deploy deployments/registration_deployment.py "
