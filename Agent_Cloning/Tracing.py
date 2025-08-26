from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool
import os
import asyncio
from dotenv import load_dotenv, find_dotenv
from dataclasses import dataclass
from typing import Callable
import time
from openai.types.responses import ResponseTextDeltaEvent

load_dotenv(find_dotenv())

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY","")
gemini_api_key : str | None = os.environ.get("GEMINI_API_KEY")


external_client: AsyncOpenAI = AsyncOpenAI(api_key=gemini_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client)
@function_tool
def get_weather(city: str) -> str:

    return f"The Weather for {city} is sunny"

@function_tool
def creative_Writer(name: str) -> str:

    return f"Greeting, {name}! May your day be filled with inspiration and creativity"

base_agent: Agent = Agent(
    name= "weather_agent",
    instructions="you are a helpful assistant.",
    model= llm_model,
    tools=[get_weather]
)
 
res = Runner.run_sync(base_agent,"what is the weather in karachi")
print(res)