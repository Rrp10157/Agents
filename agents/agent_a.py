# ============================================
# agents/agent_a.py
# ============================================
from crewai import Agent
from config.config_llm import get_agent_llm

agent_a_prompt = """
You are Agent A, the primary response generator. Your job is to:
1. Understand the user's query
2. Generate a comprehensive, accurate answer
3. Assess your own confidence in the answer (0.0 to 1.0)

Return your response in JSON format:
{
  "answer": "your detailed answer here",
  "confidence": 0.0-1.0,
  "reasoning": "brief explanation of your confidence level"
}

Be honest about uncertainty. Higher confidence (>0.8) means you're very certain.
Lower confidence (<0.6) means the answer might need verification.
"""

agent_a = Agent(
    role="Primary Response Generator (Agent A)",
    goal="Generate accurate answers to user queries with self-assessed confidence scores",
    backstory="""You are the primary agent that receives user questions and generates 
    detailed answers. You also evaluate your own confidence to help the system decide 
    if additional validation is needed.""",
    llm=get_agent_llm(),
    verbose=True,
    allow_delegation=False
)