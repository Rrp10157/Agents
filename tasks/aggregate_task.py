# ============================================
# tasks/aggregate_task.py
# ============================================
from crewai import Task

def create_batch_aggregate_task(agent, evaluations: list):
    """Create batch aggregation task"""
    return Task(
        description=f"""
        Aggregate these batch evaluation records:
        {evaluations}
        
        Apply rule-based checks, perform hybrid Human/AI veto if needed,
        handle parallel processing results, and update global metrics.
        
        Synthesize final response with comprehensive summary.
        """,
        expected_output="Final aggregation report with global metrics and synthesis",
        agent=agent
    )