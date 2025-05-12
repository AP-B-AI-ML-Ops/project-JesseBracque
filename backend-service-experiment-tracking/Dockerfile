FROM python:3.11-slim

# Install dependencies
RUN pip install mlflow psycopg2-binary

# Expose the MLflow server port
EXPOSE 5000

# Command to run MLflow server
CMD ["mlflow", "server", "--backend-store-uri", "postgresql://postgres:password@backend-database:5432/mlflow_db", "--default-artifact-root", "/mlruns","--host", "0.0.0.0", "--port", "5000"]