# MLOps Project – June 2025

**Author:** Jesse Bracqué (2ITAI)

## Introduction

This project demonstrates how to develop a fully containerized MLOps application for training and deploying a machine learning model that predicts gold price fluctuations based on historical data.

Gold has historically been a crucial asset in global economics, often used as a benchmark for market stability. The goal of this project is not to create a production-grade financial forecasting model, but rather to showcase how machine learning models can be embedded in a DevOps workflow using tools like **Docker** and **Prefect**.

> **Disclaimer:** This project is educational. The model is not meant for real-world financial decision-making.

The entire development environment was built in **Visual Studio Code**, but the instructions provided here are general and can be followed in other development setups as well.

---

## Dataset Description

The dataset used in this project is called `Daily.csv`. It contains historical gold price data and can be found in the following directories:

- `train-dev/data-files`
- `batch-dev/data-files`

This CSV file is processed and split into **training**, **validation**, and **test** datasets using the script:

- `train-dev/scripts/preprocess_data.py`

### Adding New Data

To add new data for future model predictions or retraining:

- Ensure the data follows the **exact same format** as `Daily.csv`.
- Place it in the appropriate `data-files` directory.
- Minor modifications to deployment configurations are required to ingest new files. Without changes the workflow will fail **WHEN** new files are used.

---

## Project Goal

This application trains a machine learning model to **predict future gold prices** using historical data. The model is integrated into a fully containerized MLOps workflow, allowing:

- Automated model training and validation
- Containerized deployments using Docker
- Scheduled or triggered flows with **Prefect**
- Easy extensibility for handling new data inputs

The key objective is to demonstrate how MLOps principles can be applied to streamline machine learning workflows in a scalable and reproducible way.

---

## Setup Instructions

Follow these steps to run the project from scratch:

1. **Start Docker Desktop**

   - Make sure Docker is installed and running on your system.

2. **Clone the Repository**
   ```bash
   git clone https://github.com/AP-B-AI-ML-Ops/project-JesseBracque.git
   cd project-jessebracque
   ```

## Flows & Actions

This MLOps pipeline is structured around modular Prefect flows, each responsible for a core task such as preprocessing, training, prediction, monitoring, and data ingestion. These flows coordinate to create a robust and maintainable automation framework.

---

### `scripts/preprocess_data.py`

**Flows & Tasks:**

- `run_data_prep`: Master flow to prepare and serialize datasets.
- `split_and_read_data`: Loads the raw CSV and splits into train/val sets.
- `prepare_gold_data`: Adds `gold_diff` column (target).
- `prepare_regression_train_or_val_data`: Prepares regression-ready data.
- `dump_pickle`: Saves intermediate objects like `DictVectorizer` and datasets.

**Purpose:** Converts raw gold value data into structured, vectorized inputs for training and validation.

---

### `scripts/train.py`

**Flows & Tasks:**

- `run_train`: Trains a baseline Random Forest model, logs it to MLflow.
- `load_pickle`: Loads preprocessed data and vectorizer.

**Purpose:** Establishes a performance benchmark with basic metrics and artifacts logged in MLflow.

---

### `scripts/hpo.py`

**Flows & Tasks:**

- `run_optimization`: Performs Optuna-based hyperparameter tuning.
- `objective`: Objective function that guides trial performance.
- `load_pickle`: Loads training data for optimization.

**Purpose:** Identifies optimal model hyperparameters to improve test RMSE.

---

### `scripts/register_model.py`

**Flows & Tasks:**

- `run_register_model`: Finds and retrains the best model from HPO runs, then registers it in MLflow.
- `train_and_log_model`: Retrains and logs candidate models.
- `dump_pickle`, `load_pickle`: Used for managing data serialization.

**Purpose:** Keeps the registry updated with the best-performing model.

---

### `deployments/training_deployment.py`

**Flow Name:** `training_pipeline`

**Flow Chain:**

- `run_data_prep` → `run_train` → `run_optimization`

**Purpose:** Automates the data preparation, training, and optimization processes in a single pipeline.

---

### `deployments/registration_deployment.py`

**Flow Name:** `registration_pipeline`

**Flow Chain:**

- `run_register_model`

**Purpose:** Automates the best model selection and registration into MLflow.

---

### `import_daily_to_db.py`

**Flow:**

- `import_data_into_db`: Reads the raw `Daily.csv` file, computes `gold_diff`, and inserts data into a PostgreSQL `batch_data` table.

**Purpose:** Bootstraps the monitoring system by preparing and loading raw daily data into the database for downstream analysis by Evidently.

**Interactions:**

- Used by the monitoring pipeline (`monitor.py`) to analyze historical trends.
- Ensures `batch_data` is always up-to-date for reporting.

---

### `batch.py`

**Flow:**

- `run_batch(filename, output_path)`: Runs the entire batch prediction cycle:
  - Loads latest model from MLflow.
  - Reads daily input file.
  - Applies preprocessing and vectorization.
  - Predicts next-day EUR gold value changes.
  - Saves output to `/batch-data/predictions`.
  - Triggers `run_monitoring()` for model drift checks.

**Tasks:**

- `prepare_gold_data`, `prepare_features`: Data preprocessing.
- `load_vectorizer`: Loads vectorizer used during training.
- `load_model`, `get_latest_version`: Retrieves latest model from MLflow.
- `read_data`: Loads new data for prediction.

**Purpose:** Enables real-time model inference and monitoring based on fresh market data.

**Interactions:**

- Depends on a previously trained and registered model.
- Calls `monitor.py` after prediction to track data drift and performance.

---

### `monitor.py`

**Flow Chain:**

- `run_monitoring` → `extract_data_from_report` → `generate_report`

**Details:**

- `generate_report`: Splits `batch_data` into reference/current windows and runs an Evidently `DataDriftPreset` report.
- `extract_data_from_report`: Converts the report into structured JSON-like rows.
- `run_monitoring`: Saves metric results to a PostgreSQL table `evidently_metrics`.

**Purpose:** Performs ongoing health checks on data consistency and model drift by comparing fresh prediction data against historical trends.

**Interactions:**

- Pulls input data from `batch_data` (loaded by `import_daily_to_db.py`).
- Called at the end of the `run_batch()` flow to ensure drift checks are always current.
- Enables external dashboarding or alerting via the `evidently_metrics` table.

---

This structure ensures each part of the MLOps lifecycle — from ingestion to prediction to monitoring — is modular, traceable, and easy to maintain.

## Execution Instructions

Follow these steps **in order** to properly start and run the full MLOps pipeline:

1. **Open a terminal** in VSCode at the root folder of the project.

2. Run the command:
   ```bash
   docker compose up --build
   ```

Wait approximately **3 minutes** for all services to build, start, and initialize.

3. Open your browser and navigate to:

- http://localhost:5000

This opens the **MLflow UI** where you can:

- View experiment runs under the **Experiments** tab.
- Browse registered models under the **Models** tab.
  All runs and models are automatically saved here.

4. Navigate to:

- http://localhost:4200

This opens the **Prefect UI**.

5. Under the **Deployments** section:

- Find **`complete-training-pipeline`** deployment.
- Click **Run**, then click **View** on the popup in the bottom right to monitor the flow.
- Wait for the run to complete successfully.

6. After success, back in Deployments:

- Run the **`model-registration`** deployment.
- Click **View** again and wait for it to finish successfully.

7. Then, sequentially run:

- **`push-data-to-db`** deployment.
- After it finishes successfully, run the **`daily-gold-predictions`** deployment.

---

> **Important:** These steps must be performed **in this exact order** to ensure all components are properly set up and the pipeline runs smoothly. The ony step that can be executed any earlier is **`push-data-to-db`**.

## Viewing Results and Model Usage

Now that all flows and deployments have been executed successfully, you can now explore the results and use the model for making predictions.

### View Model in MLflow

Navigate to:

- http://localhost:5000

- Go to the **Models** tab to find the registered model:  
  `gold-values-model-mlops-project`
- This model was trained and registered through the executions of:
  - `complete-training-pipeline`
  - `model-registration`
- It is now available for both batch and real-time prediction scenarios.

> **Note:** Initially, you won't see any experiments or models here until the deployments have been executed. Once executed successfully, the runs and model artifacts will appear automatically.

---

## Real-time Inference API

In addition to batch processing, this project includes a **Flask-based API** to serve real-time predictions using the trained and registered ML model.

### API Details

This service is available at:

- http://localhost:9696

It exposes a single endpoint: /predict

### What It Does

This Flask application:

- Connects to the MLflow server at `http://experiment-tracking:5000`
- Loads the latest version of the model `gold-values-model-mlops-project`
- Loads the `DictVectorizer` (`dv.pkl`) used during training
- Accepts HTTP GET requests to the `/predict` endpoint with query parameters
- Prepares the features in the same format as used in training
- Returns a prediction of the gold price difference (`gold_diff`)

### Example Request

To get a prediction, open your browser or use a tool like `curl` or Postman with a request like:

- http://localhost:9696/predict?Date=2023-10-01&EUR=1.2

This will return a JSON response:

```json
{
  "gold_diff": -0.0153
}
```

## Environment File (.env) Consideration

> **Note for Educational Use**

In this educational project, the `.env` file **is intentionally included in the repository**. While it's generally good practice to exclude `.env` files from version control using `.gitignore`—especially in real-world projects with secrets or sensitive credentials—this project **does not contain any confidential information**.

### Purpose of Including `.env`

- To make it **easier and faster for reviewers or teachers** to get the project running without needing to manually create or configure environment variables.
- To **reduce setup friction** so all components (Docker, MLflow, Prefect, Flask API, etc.) work out-of-the-box.

### Reminder for Real Projects

For real-world or production projects, always:

- Add `.env` to your `.gitignore`
- Store sensitive variables (e.g., API keys, passwords) securely
- Share environment variables through secure channels or deployment platforms

In production use:

```bash
echo ".env" >> .gitignore
```
