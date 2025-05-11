"""Flask web API for predicting gold values using a registered MLflow model."""

import pickle

import mlflow
import pandas as pd
from flask import Flask, request
from mlflow.tracking import MlflowClient

app = Flask(
    "gold-prediction"
)  # url example: http://127.0.0.1:9696/predict?Date=2023-10-01&EUR=1.2

mlflow.set_tracking_uri("http://experiment-tracking:5000")
client = MlflowClient("http://experiment-tracking:5000")
MODEL_NAME = "gold-values-model-mlops-project"


def load_vectorizer():
    """Load the DictVectorizer used during training"""
    try:
        with open("/app/dv.pkl", "rb") as f_in:
            return pickle.load(f_in)
    except Exception as e:
        print(f"Error loading DictVectorizer: {e}")
        raise


def load_model():
    """Load the latest version of the registered model from MLflow"""
    try:
        # Get the latest version of the registered model
        latest_version = client.get_latest_versions(MODEL_NAME, stages=["None"])[0]
        print(
            f"Loading model version: {latest_version.version} from {latest_version.source}"
        )

        # Load the model using the source URI from the model version
        model = mlflow.pyfunc.load_model(latest_version.source)
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        raise


def predict(features):
    """Make predictions using the loaded model"""
    model = load_model()
    dv = load_vectorizer()
    features_transformed = dv.transform(features)
    predictions = model.predict(features_transformed)
    return float(predictions[0])


def prepare_features(data):
    """Prepare features for prediction"""
    df = pd.DataFrame(
        [{"Date": pd.to_datetime(data["Date"]), "EUR": float(data["EUR"])}]
    )

    # Convert date to string as it was done during training
    df["Date"] = df["Date"].astype(str)

    # Create feature dictionaries - same as in training
    categorical = ["Date"]
    numerical = ["EUR"]

    dicts = df[categorical + numerical].to_dict(orient="records")
    return dicts


@app.route("/predict", methods=["GET"])
def predict_endpoint_get():
    """Endpoint for making predictions"""
    if not request.args:
        return {
            "error": "No parameters provided. Use /predict?Date=2023-10-01&EUR=1.2"
        }, 400

    try:
        data = {
            "Date": str(request.args.get("Date")),
            "EUR": float(request.args.get("EUR")),
        }
    except ValueError as e:
        return {"error": f"Invalid input: {e}"}, 400

    features = prepare_features(data)
    prediction = predict(features)

    return {"gold_diff": prediction}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9696)
