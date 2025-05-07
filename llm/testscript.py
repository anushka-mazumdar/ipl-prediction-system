from llm.ollama_reasoner import query_ollama_reasoning

match_sample = {
    "team1": "Mumbai Indians",
    "team1_score": 178,
    "team1_wickets": 6,
    "player_of_match": "Rohit Sharma",
    "toss_winner": "Mumbai Indians",
    "toss_decision": "bat"
}

predicted_winner = "Mumbai Indians"

reason = query_ollama_reasoning(match_sample, predicted_winner)
print("Reasoning:\n", reason)
