# agents/light_coach.py
from crewai import Agent

# short prompt template that the agent will use to evaluate quickly
light_prompt = """
You are a fast evaluator. Given 'output' and optional 'context', return:
- pass_fail: boolean (true = passes light checks)
- score: float 0..1
- reason: one-line text
Use simple checks: clarity, grammar, length, similarity.
Output JSON.
"""

light_coach = Agent(
    role="Lightweight Coach",
    goal="Quickly evaluate clarity, grammar, and basic logic of outputs",
    backstory="A fast low-latency evaluator that should return a JSON indicating pass/fail.",
    prompt=light_prompt,
    verbose=False
)
