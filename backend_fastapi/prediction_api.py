import os
os.chdir("C:/Users/Anushka/Desktop/anushka/ML/projects_vscode/IPL prediction system")
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np

app = FastAPI()

# Load models
xgb_model = joblib.load("ml_model/xgb_model.pkl")
lgbm_model = joblib.load("ml_model/lgbm_model.pkl")
nn_model = joblib.load("ml_model/nn_model.pkl")
team_encoder = joblib.load("ml_model/team_encoder.pkl")

# Prediction input schema
class MatchPredictionInput(BaseModel):
    team1: str
    team1_score: int
    team1_wickets: int

# Confidence Interval Calculation
def get_confidence_interval(predictions):
    mean = np.mean(predictions)
    std_dev = np.std(predictions)
    ci_low = mean - 1.96 * std_dev
    ci_high = mean + 1.96 * std_dev
    return mean, (ci_low, ci_high)

@app.post("/predict")
async def predict_outcome(data: MatchPredictionInput):
    try:
        # Encode team
        team1_encoded = team_encoder.transform([data.team1])[0]

        # Prepare input
        X = pd.DataFrame([[team1_encoded, data.team1_score, data.team1_wickets]],
                         columns=["team1_encoded", "team1_score", "team1_wickets"])

        # Predictions from individual models
        xgb_pred = xgb_model.predict(X)[0]
        lgbm_pred = lgbm_model.predict(X)[0]
        nn_pred = nn_model.predict(X)[0]

        # Ensemble prediction (majority vote)
        ensemble_pred = np.round(np.mean([xgb_pred, lgbm_pred, nn_pred]))

        # Confidence Interval
        mean_pred, (ci_low, ci_high) = get_confidence_interval([xgb_pred, lgbm_pred, nn_pred])

        return {
            "predicted_winner": int(ensemble_pred),
            "confidence_interval": [ci_low, ci_high]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/player-trends/{player_name}")
async def get_player_trends(player_name: str):
    try:
        trends = pd.read_csv("data_processing/processed_data/player_trends.csv")
        player_data = trends[trends['player'].str.contains(player_name, case=False)]

        if player_data.empty:
            return {"message": f"No trends found for player: {player_name}"}

        return player_data.to_dict(orient="records")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


