import os 
import asyncio
from dotenv import find_dotenv, load_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled

load_dotenv(find_dotenv())

set_tracing_disabled(disabled=True)
gemini_api_key = os.environ.get("GEMINI_API_KEY")
tavily_api_key = os.environ.get("TAVILY_API_KEY")

Provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

llm_model = OpenAIChatCompletionsModel(
    openai_client=Provider,
    model="gemini-2.5-flash"
)


math_agent : Agent = Agent(
    name="Maths Agent",
    instructions="A maths agent that can solve the maths problems",
    model=llm_model
)

# output = Runner.run_sync(starting_agent=math_agent, input="why Learn maths")
# print(output.final_output)

async def call_agent():
    output = await Runner.run(starting_agent=math_agent, input="why Learn Maths")
    print(output.final_output)

asyncio.run(call_agent())