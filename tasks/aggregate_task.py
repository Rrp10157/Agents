# tasks/aggregate_task.py
from crewai import Task

aggregate_task = Task(
    description="Aggregate multiple evaluation records into a final summary and global metrics update.",
    expected_output="final report JSON"
)
