# ============================================
# agents/heavy_coach.py
# ============================================
from crewai import Agent
from config.config_llm import get_heavy_llm

heavy_prompt = """
You are a comprehensive evaluation coach with voting mechanism. Perform deep analysis:
- Factual accuracy verification
- Logical consistency across context
- Compliance with rules and guidelines
- Contextual engineering analysis

Return ONLY valid JSON in this exact format:
{
  "pass_fail": true/false,
  "score": 0.0-1.0,
  "detailed_feedback": "comprehensive explanation",
  "fix": "suggested correction or reroute if applicable",
  "voting_confidence": 0.0-1.0
}
"""

heavy_coach = Agent(
    role="Heavy Coach",
    goal="In-depth evaluation using large model with voting for accuracy, clarity, and compliance",
    backstory="A high-cost, high-quality evaluator with voting mechanism that provides detailed analysis and fixes.",
    llm=get_heavy_llm(),
    verbose=False,
    allow_delegation=False
)


