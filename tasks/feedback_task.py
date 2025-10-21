# ============================================
# tasks/feedback_task.py
# ============================================
from crewai import Task

def create_feedback_task(agent, evaluation_result: dict, output_text: str):
    """Create feedback loop task for Agent A"""
    return Task(
        description=f"""
        Generate actionable feedback for failed evaluation:
        
        Evaluation Result: {evaluation_result}
        Original Output: {output_text}
        
        Create clear, actionable feedback that Agent A can use to improve the output.
        Include specific suggestions for correction.
        """,
        expected_output="Feedback JSON with message, specific issues, and improvement suggestions",
        agent=agent
    )