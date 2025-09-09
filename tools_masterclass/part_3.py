import os
import asyncio
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool

_: bool = load_dotenv(find_dotenv())

# ONLY FOR TRACING
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")

gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")

# 1. Which LLM Service?
external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# 2. Which LLM Model?
llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)


@function_tool
def get_weather(city: str) -> str:
    raise ValueError("weather service is currently unavailable.")


base_agent: Agent = Agent(
    name="WeatherAgent",
    # instructions="You are a helpful assistant. if some tools is not available - call it at least 5 times before giving up",
    model=llm_model,
    tools=[get_weather],
    
)

async def main():
    res = await Runner.run(base_agent, "What is weather in karachi")
    print(res.final_output)

if __name__ =="__main__":
    asyncio.run(main())