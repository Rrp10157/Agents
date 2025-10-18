# run_local.py
import asyncio
from crew_setup import build_coach_crew, evaluate_with_crew

async def main():
    crew = build_coach_crew()
    # warm up models if necessary
    output = "The Great Wall of China is visible from space."
    result = await evaluate_with_crew(crew, output=output, confidence=0.6, agent_id="writer-1", context="")
    print("EVAL RESULT:", result)

if __name__ == "__main__":
    asyncio.run(main())
