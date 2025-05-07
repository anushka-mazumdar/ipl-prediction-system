def format_match_reasoning_prompt(match_data: dict, prediction: str) -> str:
    prompt = f"""
You are a cricket analyst. Using the match details and prediction below, explain the reasoning behind the model's prediction.

Match Details:
- Team 1: {match_data.get("team1")}
- Team 1 Score: {match_data.get("team1_score")}
- Team 1 Wickets: {match_data.get("team1_wickets")}
- Player of Match: {match_data.get("player_of_match")}
- Toss Winner: {match_data.get("toss_winner")}
- Toss Decision: {match_data.get("toss_decision")}

Model Prediction:
- Predicted Winner: {prediction}

Provide a clear explanation for this prediction, considering team performance, score strength, toss impact, and key players.
"""
    return prompt.strip()
