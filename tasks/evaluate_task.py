# tasks/evaluate_task.py
from crewai import Task

evaluate_task = Task(
    description=(
        "Take an input object: {output, confidence, agent_id, context}. "
        "Return a structured evaluation record. Follow coordinator's routing."
    ),
    expected_output="JSON evaluation record"
)
