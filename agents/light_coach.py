# ============================================
# agents/light_coach.py
# ============================================
from crewai import Agent
from config.config_llm import get_light_llm

light_prompt = """
You are a fast evaluator performing lightweight checks. Evaluate the given output for:
- Grammar and clarity
- Basic coherence
- Length appropriateness
- Surface-level correctness

Return ONLY valid JSON in this exact format:
{
  "pass_fail": true/false,
  "score": 0.0-1.0,
  "reason": "brief explanation",
  "escalate": true/false
}

Set "escalate" to true if you're uncertain or if the content needs deeper analysis.
"""

light_coach = Agent(
    role="Lightweight Coach",
    goal="Fast evaluation using simple metrics (BLEU, latency, context similarity)",
    backstory="A fast low-latency evaluator that performs basic checks and decides if escalation is needed.",
    llm=get_light_llm(),
    verbose=False,
    allow_delegation=False
)

