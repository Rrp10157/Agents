# ============================================
# run_local.py
# ============================================
import asyncio
from crew_setup import build_coach_crew, evaluate_with_crew

async def main():
    # Build the crew (optional - kept for compatibility)
    crew = build_coach_crew()
    print("Coach Crew built successfully!\n")
    
    # Test cases
    test_cases = [
        {
            "output": "The Great Wall of China is visible from space.",
            "confidence": 0.6,
            "agent_id": "writer-1",
            "context": "Common misconception test"
        },
        {
            "output": "Python is a high-level programming language.",
            "confidence": 0.9,
            "agent_id": "writer-2",
            "context": "Programming facts"
        },
        {
            "output": "This text contains confidential information.",
            "confidence": 0.8,
            "agent_id": "writer-3",
            "context": "Security test"
        },
        {
            "output": "The sky appears blue due to Rayleigh scattering.",
            "confidence": 0.5,
            "agent_id": "writer-4",
            "context": "Scientific explanation"
        }
    ]
    
    print("=" * 60)
    print("RUNNING EVALUATION TESTS")
    print("=" * 60)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"TEST CASE {i}")
        print(f"{'='*60}")
        print(f"Output: {test['output']}")
        print(f"Confidence: {test['confidence']}")
        print(f"Agent ID: {test['agent_id']}")
        print(f"Context: {test['context']}")
        print(f"\nEvaluating...")
        
        try:
            result = await evaluate_with_crew(
                crew,  # Pass crew for compatibility
                output=test['output'],
                confidence=test['confidence'],
                agent_id=test['agent_id'],
                context=test['context']
            )
            
            print(f"\n{'─'*60}")
            print("RESULT:")
            print(f"{'─'*60}")
            print(f"Stage: {result.get('stage', 'N/A')}")
            print(f"Pass/Fail: {'PASS' if result.get('pass_fail') else 'FAIL'}")
            print(f"Score: {result.get('score', 0):.2f}")
            print(f"Feedback: {result.get('feedback', 'N/A')}")
            if 'fix' in result and result['fix']:
                print(f"Suggested Fix: {result['fix']}")
            
        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
    
    print(f"\n{'='*60}")
    print("ALL TESTS COMPLETED")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    print("\n🚀 Starting Coach Crew Local Evaluation System...\n")
    asyncio.run(main())
