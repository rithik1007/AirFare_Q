import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

KAGGLE_API_URL = "https://api.kaggle.com/models/meta-llama/Llama-3.1-8B-Instruct/1/infer"

class TravelAgentLLM:
    def __init__(self):
        self.auth = (
            os.getenv("KAGGLE_USERNAME"),
            os.getenv("KAGGLE_KEY")
        )
        
        if not self.auth[0] or not self.auth[1]:
            raise ValueError("Kaggle API credentials missing. Set KAGGLE_USERNAME and KAGGLE_KEY in .env")

    def ask(self, user_prompt):
        payload = {
            "inputs": user_prompt,
            "parameters": {
                "max_length": 300,
                "temperature": 0.4
            }
        }

        response = requests.post(
            KAGGLE_API_URL,
            auth=self.auth,
            json=payload
        )

        response.raise_for_status()
        return response.json()["outputs"]
