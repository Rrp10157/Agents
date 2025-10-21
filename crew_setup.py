# ============================================
# crew_setup.py
# ============================================
import os
import json
from crewai import Crew, Process
from dotenv import load_dotenv
from agents.agent_a import agent_a
from agents.light_coach import light_coach
from agents.heavy_coach import heavy_coach
from agents.agent_2 import agent_2
from tasks.generate_task import create_generation_task
from tasks.evaluate_task import create_light_evaluate_task, create_heavy_evaluate_task
from tasks.aggregate_task import create_batch_aggregate_task
from utils.memory_buffer import store_eval, append_history

load_dotenv()
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", 0.8))
LIGHT_THRESHOLD = float(os.getenv("LIGHT_THRESHOLD", 0.7))

def build_coach_crew():
    """Build crew with all agents"""
    crew = Crew(
        agents=[agent_a, light_coach, heavy_coach, agent_2],
        tasks=[],
        process=Process.sequential,
        verbose=False
    )
    return crew


async def generate_and_evaluate(user_query: str, context: str = None, agent_id: str = None):
    """
    Complete flow: Generate answer with Agent A, then evaluate it
    
    Returns:
        dict with: query, answer, confidence, evaluation_result
    """
    
    # STEP 1: Agent A generates answer with confidence
    print(f"\n🤖 Agent A generating answer for: {user_query[:50]}...")
    
    generation_task = create_generation_task(agent_a, user_query, context or "")
    generation_crew = Crew(
        agents=[agent_a],
        tasks=[generation_task],
        process=Process.sequential,
        verbose=True
    )
    
    try:
        gen_result = generation_crew.kickoff()
        gen_output = str(gen_result)
        
        # Parse Agent A's response
        try:
            if '{' in gen_output and '}' in gen_output:
                json_start = gen_output.index('{')
                json_end = gen_output.rindex('}') + 1
                gen_json = json.loads(gen_output[json_start:json_end])
            else:
                gen_json = json.loads(gen_output)
            
            answer = gen_json.get("answer", gen_output)
            confidence = float(gen_json.get("confidence", 0.5))
            reasoning = gen_json.get("reasoning", "")
            
        except (json.JSONDecodeError, ValueError):
            # Fallback if Agent A doesn't return proper JSON
            answer = gen_output
            confidence = 0.5
            reasoning = "Could not parse confidence from response"
        
        print(f"✅ Answer generated (Confidence: {confidence:.2f})")
        
    except Exception as e:
        return {
            "query": user_query,
            "answer": None,
            "confidence": 0.0,
            "error": f"Generation failed: {str(e)}",
            "evaluation_result": None
        }
    
    # STEP 2: Evaluate the generated answer
    print(f"\n🔍 Evaluating answer...")
    
    eval_result = await evaluate_with_crew(
        output=answer,
        confidence=confidence,
        agent_id=agent_id or "agent_a_default",
        context=f"Query: {user_query}\nContext: {context or 'None'}"
    )
    
    # STEP 3: Return complete result
    return {
        "query": user_query,
        "answer": answer,
        "confidence": confidence,
        "reasoning": reasoning,
        "evaluation_result": eval_result,
        "final_status": "APPROVED" if eval_result.get("pass_fail") else "REJECTED",
        "requires_revision": eval_result.get("requires_feedback_loop", False)
    }


async def evaluate_with_crew(crew=None, *, output: str, confidence: float, 
                            agent_id: str = None, context: str = None):
    """
    Main evaluation flow following the architecture diagram:
    1. Check confidence threshold (>= 0.8) - skip evaluation if high
    2. Lightweight coach evaluation
    3. Escalate to heavy coach if needed
    4. Store in memory buffer
    """
    
    # STEP 1: Check confidence threshold (bypass evaluation if confidence >= 0.8)
    if confidence >= CONFIDENCE_THRESHOLD:
        record = {
            "agent_id": agent_id,
            "stage": "confidence_bypass",
            "pass_fail": True,
            "score": confidence,
            "feedback": f"High confidence ({confidence:.2f} >= {CONFIDENCE_THRESHOLD}) - bypassing evaluation"
        }
        append_history(agent_id or "unknown", record)
        store_eval(f"{agent_id}:last", record)
        return record
    
    # STEP 2: Lightweight coach evaluation
    light_task = create_light_evaluate_task(light_coach, output, context)
    light_crew = Crew(
        agents=[light_coach],
        tasks=[light_task],
        process=Process.sequential,
        verbose=False
    )
    
    try:
        light_result = light_crew.kickoff()
        light_output = str(light_result)
        
        try:
            if '{' in light_output and '}' in light_output:
                json_start = light_output.index('{')
                json_end = light_output.rindex('}') + 1
                light_json = json.loads(light_output[json_start:json_end])
            else:
                light_json = json.loads(light_output)
        except json.JSONDecodeError:
            light_json = {
                "pass_fail": False,
                "score": 0.0,
                "reason": f"Unparseable light coach response",
                "escalate": True
            }
    except Exception as e:
        light_json = {
            "pass_fail": False,
            "score": 0.0,
            "reason": f"Light evaluation error: {str(e)}",
            "escalate": True
        }
    
    # STEP 3: Check if light coach failed
    if not light_json.get("pass_fail", False):
        record = {
            "agent_id": agent_id,
            "stage": "light_failed",
            "pass_fail": False,
            "score": float(light_json.get("score", 0.0)),
            "feedback": light_json.get("reason", "Light coach failed"),
            "requires_feedback_loop": True
        }
        append_history(agent_id or "unknown", record)
        store_eval(f"{agent_id}:last", record)
        return record
    
    # STEP 4: Check if escalation to heavy coach is needed
    should_escalate = light_json.get("escalate", False) or light_json.get("score", 1.0) < 0.7
    
    if should_escalate:
        # Heavy coach evaluation with voting
        heavy_task = create_heavy_evaluate_task(heavy_coach, output, context)
        heavy_crew = Crew(
            agents=[heavy_coach],
            tasks=[heavy_task],
            process=Process.sequential,
            verbose=False
        )
        
        try:
            heavy_result = heavy_crew.kickoff()
            heavy_output = str(heavy_result)
            
            try:
                if '{' in heavy_output and '}' in heavy_output:
                    json_start = heavy_output.index('{')
                    json_end = heavy_output.rindex('}') + 1
                    heavy_json = json.loads(heavy_output[json_start:json_end])
                else:
                    heavy_json = json.loads(heavy_output)
            except json.JSONDecodeError:
                heavy_json = {
                    "pass_fail": False,
                    "score": 0.0,
                    "detailed_feedback": f"Unparseable heavy response"
                }
        except Exception as e:
            heavy_json = {
                "pass_fail": False,
                "score": 0.0,
                "detailed_feedback": f"Heavy evaluation error: {str(e)}"
            }
        
        record = {
            "agent_id": agent_id,
            "stage": "heavy_evaluation",
            "pass_fail": bool(heavy_json.get("pass_fail", False)),
            "score": float(heavy_json.get("score", 0.0)),
            "feedback": heavy_json.get("detailed_feedback", ""),
            "fix": heavy_json.get("fix", ""),
            "voting_confidence": heavy_json.get("voting_confidence", 0.0),
            "requires_feedback_loop": not heavy_json.get("pass_fail", False)
        }
        append_history(agent_id or "unknown", record)
        store_eval(f"{agent_id}:last", record)
        return record
    
    # STEP 5: Light passed without escalation
    record = {
        "agent_id": agent_id,
        "stage": "light_passed",
        "pass_fail": True,
        "score": float(light_json.get("score", 1.0)),
        "feedback": light_json.get("reason", "Light coach approved"),
        "requires_feedback_loop": False
    }
    append_history(agent_id or "unknown", record)
    store_eval(f"{agent_id}:last", record)
    return record


async def batch_evaluate(outputs: list, agent_id: str = None):
    """
    Batch evaluation for multiple outputs (parallel processing as per architecture)
    """
    results = []
    for idx, item in enumerate(outputs):
        result = await evaluate_with_crew(
            output=item.get("output"),
            confidence=item.get("confidence", 0.5),
            agent_id=f"{agent_id}_batch_{idx}",
            context=item.get("context", "")
        )
        results.append(result)
    
    # Aggregate with Agent 2
    aggregate_task = create_batch_aggregate_task(agent_2, results)
    aggregate_crew = Crew(
        agents=[agent_2],
        tasks=[aggregate_task],
        process=Process.sequential,
        verbose=True
    )
    
    final_result = aggregate_crew.kickoff()
    return {
        "individual_results": results,
        "aggregated_summary": str(final_result),
        "total_processed": len(outputs),
        "passed": sum(1 for r in results if r.get("pass_fail")),
        "failed": sum(1 for r in results if not r.get("pass_fail"))
    }