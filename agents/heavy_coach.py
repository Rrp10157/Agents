# agents/heavy_coach.py
from crewai import Agent

heavy_prompt = """
You are a deep evaluation coach. Given 'output' and 'context', perform:
- factuality check
- logical consistency check across context
- compliance with rules
Return JSON:
{
  "pass_fail": boolean,
  "score": float,
  "detailed_feedback": "..."
}
If you can produce a synthethic fix (short), include "fix": "...".
"""

heavy_coach = Agent(
    role="Heavy Coach",
    goal="In-depth factual and reasoning evaluation using a large LLM or voting ensemble",
    backstory="A high-cost, high-quality evaluator that gives explanations and suggested fixes.",
    prompt=heavy_prompt,
    verbose=False
)
