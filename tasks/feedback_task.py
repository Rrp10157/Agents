# tasks/feedback_task.py
from crewai import Task

feedback_task = Task(
    description="Given a failing evaluation, create actionable, short feedback and suggest a fix.",
    expected_output="feedback JSON with 'message' and optional 'fix'"
)
