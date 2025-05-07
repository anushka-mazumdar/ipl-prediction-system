import subprocess
import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from .prompts import format_match_reasoning_prompt


OLLAMA_MODEL = "llama3"  # Change to "mistral" or any local model you've pulled

def query_ollama_reasoning(match_data: dict, prediction: str) -> str:
    prompt = format_match_reasoning_prompt(match_data, prediction)

    process = subprocess.Popen(
        ["ollama", "run", OLLAMA_MODEL],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    stdout, stderr = process.communicate(prompt)
    
    if stderr:
        print("Error from Ollama:", stderr)
    
    return stdout.strip()
