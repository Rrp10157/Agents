# agents/coordinator.py
from crewai import Agent

coord_prompt = """
You are the Coordinator. Input contains: { "output": "...", "confidence": float, "agent_id": "..." }.
Follow this algorithm:
1) If confidence >= CONFIDENCE_THRESHOLD -> approve with message "high confidence, skip heavy".
2) Else -> call lightweight coach. If light_coach returns pass_fail == False -> return that result as fail.
3) If light passes but indicates 'uncertain' or low score -> escalate to heavy coach.
4) Aggregate results and return JSON: { "final_score": float, "pass_fail": bool, "report": {...} }.
You may reference memory buffer for previous evaluations.
Respond as JSON.
"""
coordinator = Agent(
    role="Coordinator Agent",
    goal="Route outputs between light and heavy coaches, aggregate results, keep trace",
    backstory="Central router that implements the confidence heuristic and orchestrates coaches.",
    prompt=coord_prompt,
    verbose=True
)
