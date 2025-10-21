# ============================================
# agents/agent_2.py
# ============================================
from crewai import Agent
from config.config_llm import get_agent2_llm

agent_2 = Agent(
    role="Aggregation and Synthesis Agent",
    goal="Aggregate batch evaluations, apply rule-based checks, and synthesize final response",
    backstory="""You aggregate outputs from multiple evaluations, perform hybrid Human/AI veto 
    checks, handle parallel processing of multiple outputs, and update global metrics.""",
    llm=get_agent2_llm(),
    verbose=True,
    allow_delegation=False
)

