from flask import Flask, request
import mlflow
import pandas as pd
from mlflow.tracking import MlflowClient
from mlflow.entities import ViewType

app = Flask('gold-prediction')  # url example: http://127.0.0.1:9696/predict?Date=2023-10-01&EUR=1.2

mlflow.set_tracking_uri("http://experiment-tracking:5000")
client = MlflowClient("http://experiment-tracking:5000")

def load_model():
    MODEL_NAME = "gold-values-model-mlops-project"
    
    try:
        # First, check if the model exists
        models = client.search_registered_models()
        print("Available models:", [m.name for m in models])
        
        # Get the experiment to find the latest run
        experiment = client.get_experiment_by_name("gold-values-experiment-mlops-project")
        if experiment is None:
            raise Exception("Experiment not found")
            
        # Get the latest successful run
        runs = client.search_runs(
            experiment_ids=[experiment.experiment_id],
            run_view_type=ViewType.ACTIVE_ONLY,
            max_results=1,
            order_by=["metrics.test_rmse ASC"]
        )
        
        if not runs:
            raise Exception("No runs found in the experiment")
            
        run_id = runs[0].info.run_id
        print(f"Loading model from run: {run_id}")
        
        # Load the model directly from the run
        model_uri = f"runs:/{run_id}/model"
        model = mlflow.pyfunc.load_model(model_uri)
        return model
        
    except Exception as e:
        print(f"Error loading model: {e}")
        print("MLflow tracking URI:", mlflow.get_tracking_uri())
        print("Available experiments:", [exp.name for exp in client.search_experiments()])
        raise

def predict(features):
    model = load_model()
    predictions = model.predict(features)
    return float(predictions[0])

def prepare_features(data):
    return pd.DataFrame([{
        "Date": data["Date"],
        "EUR": data["EUR"]
    }])

@app.route("/predict", methods=["GET"])
def predict_endpoint_get():
    if not request.args:
        return {"error": "No parameters provided. Use /predict?Date=2023-10-01&EUR=1.2"}, 400
        
    try:
        data = {
            "Date": str(request.args.get("Date")),
            "EUR": float(request.args.get("EUR"))
        }

    except ValueError as e:
        return {"error": f"Invalid input: {e}"}, 400

    features = prepare_features(data)
    prediction = predict(features)

    return {
        "gold_diff": prediction
    }

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9696)