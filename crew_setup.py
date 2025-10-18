# crew_setup.py
import os
from crewai import Crew, Process
from agents.light_coach import light_coach
from agents.heavy_coach import heavy_coach
# coordinator can be used as an LLM-backed router for explanation; but we'll implement programmatic routing:
from utils.rules_engine import should_skip_heavy, apply_rules, LIGHT_THRESHOLD, HEAVY_THRESHOLD
from utils.memory_buffer import store_eval, get_eval, append_history
import json
from tasks.evaluate_task import evaluate_task
from tasks.feedback_task import feedback_task
from tasks.aggregate_task import aggregate_task

def build_coach_crew():
    crew = Crew(
        agents=[light_coach, heavy_coach],
        tasks=[evaluate_task, feedback_task, aggregate_task],
        process=Process.hierarchical,
        verbose=False
    )
    return crew

# Programmatic coordinator function — recommended for stable routing
async def evaluate_with_crew(crew, *, output: str, confidence: float, agent_id: str = None, context: str = None):
    # quick rule check
    ok, rule_msg = apply_rules(output)
    if not ok:
        record = {
            "agent_id": agent_id,
            "stage": "rules",
            "pass_fail": False,
            "score": 0.0,
            "feedback": rule_msg
        }
        append_history(agent_id or "unknown", record)
        store_eval(f"{agent_id}:last", record)
        return record

    if should_skip_heavy(confidence):
        record = {
            "agent_id": agent_id,
            "stage": "skip_heavy",
            "pass_fail": True,
            "score": confidence,
            "feedback": "High confidence — accepted by coordinator"
        }
        append_history(agent_id or "unknown", record)
        store_eval(f"{agent_id}:last", record)
        return record

    # Light evaluation via Crew's agent invocation
    # Depending on CrewAI SDK, you might call `crew.run_agent(light_coach, inputs=...)` or `light_coach.run(...)`
    light_inputs = {"output": output, "context": context or ""}
    light_result = await crew.run_agent(light_coach, inputs=light_inputs)  # <-- adapt if API differs

    # Expect the agent to return a JSON string or dict. Normalize:
    if isinstance(light_result, str):
        try:
            light_json = json.loads(light_result)
        except:
            # fallback: treat as fail if unparseable
            light_json = {"pass_fail": False, "score": 0.0, "reason": "unparseable light coach response"}
    else:
        light_json = light_result

    if not light_json.get("pass_fail", False):
        record = {
            "agent_id": agent_id,
            "stage": "light",
            "pass_fail": False,
            "score": float(light_json.get("score", 0.0)),
            "feedback": light_json.get("reason", "Light coach failed")
        }
        append_history(agent_id or "unknown", record)
        store_eval(f"{agent_id}:last", record)
        return record

    # If light passes but is low confidence -> escalate to heavy
    if light_json.get("score", 1.0) < LIGHT_THRESHOLD or light_json.get("reason","").lower().find("uncertain")!=-1:
        heavy_inputs = {"output": output, "context": context or ""}
        heavy_result = await crew.run_agent(heavy_coach, inputs=heavy_inputs)

        if isinstance(heavy_result, str):
            try:
                heavy_json = json.loads(heavy_result)
            except:
                heavy_json = {"pass_fail": False, "score": 0.0, "detailed_feedback": "unparseable heavy response"}
        else:
            heavy_json = heavy_result

        record = {
            "agent_id": agent_id,
            "stage": "heavy",
            "pass_fail": bool(heavy_json.get("pass_fail", False)),
            "score": float(heavy_json.get("score", 0.0)),
            "feedback": heavy_json.get("detailed_feedback", "")
        }
        append_history(agent_id or "unknown", record)
        store_eval(f"{agent_id}:last", record)
        return record

    # Light passed okay and no heavy needed
    record = {
        "agent_id": agent_id,
        "stage": "light_ok",
        "pass_fail": True,
        "score": float(light_json.get("score", 1.0)),
        "feedback": light_json.get("reason", "Light coach ok")
    }
    append_history(agent_id or "unknown", record)
    store_eval(f"{agent_id}:last", record)
    return record
