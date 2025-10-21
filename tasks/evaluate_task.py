# ============================================
# tasks/evaluate_task.py
# ============================================
from crewai import Task

def create_light_evaluate_task(agent, output_text: str, context: str = ""):
    """Create lightweight evaluation task"""
    return Task(
        description=f"""
        Perform lightweight evaluation on:
        
        Output: {output_text}
        Context: {context if context else 'No additional context provided'}
        
        Check for grammar, clarity, coherence, and basic correctness.
        Return JSON with pass_fail, score, reason, and escalate flag.
        """,
        expected_output="JSON evaluation with pass_fail, score, reason, and escalate fields",
        agent=agent
    )

def create_heavy_evaluate_task(agent, output_text: str, context: str = ""):
    """Create heavy evaluation task with voting"""
    return Task(
        description=f"""
        Perform comprehensive evaluation with voting on:
        
        Output: {output_text}
        Context: {context if context else 'No additional context provided'}
        
        Verify factual accuracy, logical consistency, rule compliance, and contextual appropriateness.
        Use voting mechanism for confidence scoring.
        Return JSON with pass_fail, score, detailed_feedback, fix, and voting_confidence.
        """,
        expected_output="JSON evaluation with comprehensive analysis and voting confidence",
        agent=agent
    )

