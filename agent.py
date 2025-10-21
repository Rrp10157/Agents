from crewai import Agent, Task, Crew, LLM
import os

# Set your Groq API key (or it will use GROQ_API_KEY env variable)
os.environ["GROQ_API_KEY"] = "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"

# Initialize Groq LLM using CrewAI's LLM class
llm = LLM(
    model="groq/openai/gpt-oss-20b",  # Using the model from your playground code
    temperature=1,
    max_tokens=8192,
    top_p=1,
    # reasoning_effort="medium"  # Note: This might not be supported in all contexts
)

# Alternative models you can use:
# llm = LLM(model="groq/mixtral-8x7b-32768")
# llm = LLM(model="groq/llama-3.1-70b-versatile")
# llm = LLM(model="groq/llama-3.1-8b-instant")

# Create an agent
researcher = Agent(
    role="Research Analyst",
    goal="Conduct thorough research on given topics and provide detailed insights",
    backstory="""You are an experienced research analyst with expertise in 
    gathering and analyzing information from various sources. You excel at 
    breaking down complex topics into clear, actionable insights.""",
    llm=llm,
    verbose=True,
    allow_delegation=False
)

# Create a writer agent
writer = Agent(
    role="Content Writer",
    goal="Transform research findings into engaging, well-structured content",
    backstory="""You are a skilled content writer who excels at taking 
    complex information and creating clear, compelling narratives that 
    resonate with readers.""",
    llm=llm,
    verbose=True,
    allow_delegation=False
)

# Create tasks
research_task = Task(
    description="""Research the latest developments in artificial intelligence 
    and identify the top 3 trends for 2025. Include specific examples and 
    potential impacts.""",
    agent=researcher,
    expected_output="A detailed research report with 3 AI trends, examples, and impact analysis"
)

writing_task = Task(
    description="""Take the research findings and write an engaging blog post 
    about AI trends in 2025. Make it accessible to a general audience while 
    maintaining technical accuracy.""",
    agent=writer,
    expected_output="A well-structured blog post (500-700 words) about AI trends",
    context=[research_task]  # This task depends on the research_task
)

# Create a crew with the agents and tasks
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    verbose=True
)

# Execute the crew
if __name__ == "__main__":
    print("Starting CrewAI with Groq LLM...\n")
    result = crew.kickoff()
    print("\n\n=== Final Result ===")
    print(result)