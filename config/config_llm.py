
# ============================================
# config/llm_config.py
# ============================================
import os
from crewai import LLM
from dotenv import load_dotenv

load_dotenv()

def get_groq_llm(model_name: str = None, temperature: float = 0.7):
    """
    Initialize and return Groq LLM instance.
    This is the central place where LLM is configured.
    """
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables")
    
    # Default model if not specified
    if model_name is None:
        model_name = os.getenv("GROQ_MODEL", "groq/llama-3.1-8b-instant")
    
    llm = LLM(
        model=model_name,
        temperature=temperature,
        api_key=groq_api_key
    )
    return llm

# Create different LLM instances for different agents
def get_light_llm():
    """Fast, lightweight LLM for quick evaluations"""
    return get_groq_llm(
        model_name="groq/llama-3.1-8b-instant",
        temperature=0.3
    )

def get_heavy_llm():
    """Powerful LLM for deep evaluations with voting"""
    return get_groq_llm(
        model_name="groq/llama-3.3-70b-versatile",
        temperature=0.5
    )

def get_agent_llm():
    """LLM for Agent A (primary agent)"""
    return get_groq_llm(
        model_name="groq/openai/gpt-oss-20b",
        temperature=0.7
    )

def get_agent2_llm():
    """LLM for Agent 2 (synthesis and aggregation)"""
    return get_groq_llm(
        model_name="groq/llama-3.3-70b-versatile",
        temperature=0.4
    )
