# utils/rules_engine.py
import os
from dotenv import load_dotenv

load_dotenv()
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", 0.8))
LIGHT_THRESHOLD = float(os.getenv("LIGHT_THRESHOLD", 0.7))
HEAVY_THRESHOLD = float(os.getenv("HEAVY_THRESHOLD", 0.75))

# simple rule check
FORBIDDEN_TERMS = ["confidential", "private key", "classified"]

def apply_rules(text: str):
    for term in FORBIDDEN_TERMS:
        if term.lower() in text.lower():
            return False, f"Contains forbidden term '{term}'"
    return True, "passed"

def should_skip_heavy(confidence: float):
    return confidence >= CONFIDENCE_THRESHOLD
