# ============================================
# tasks/generate_task.py
# ============================================
from crewai import Task

def create_generation_task(agent, user_query: str, context: str = ""):
    """Create task for Agent A to generate answer with confidence"""
    return Task(
        description=f"""
        Generate a comprehensive answer to this user query:
        
        Query: {user_query}
        Context: {context if context else 'No additional context'}
        
        Provide your answer along with a confidence score (0.0-1.0) indicating 
        how certain you are about the accuracy of your response.
        
        Return JSON format with: answer, confidence, and reasoning.
        """,
        expected_output="JSON with answer, confidence score (0-1), and reasoning",
        agent=agent
    )
