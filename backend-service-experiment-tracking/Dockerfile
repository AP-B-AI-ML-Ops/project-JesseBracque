FROM python:3.9-slim

# Install dependencies
RUN pip install mlflow psycopg2-binary

# Expose the MLflow server port
EXPOSE 5000

# Command to run MLflow server
CMD ["mlflow", "server", "--backend-store-uri", "postgresql://username:password@database:5432/mydatabase", "--default-artifact-root", "/mlflow"]