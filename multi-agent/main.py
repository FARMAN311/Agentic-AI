from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool
import os
import asyncio
from dotenv import load_dotenv, find_dotenv
from dataclasses import dataclass
from typing import Callable
import time
from datetime import datetime
from openai.types.responses import ResponseTextDeltaEvent

load_dotenv(find_dotenv())

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY","")
gemini_api_key : str | None = os.environ.get("GEMINI_API_KEY")


external_client: AsyncOpenAI = AsyncOpenAI(api_key=gemini_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client)

special_llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(model="gemini-2.5-pro", openai_client=external_client)


@function_tool
def get_weather(city: str) -> str:

    return f"The Weather for {city} is sunny"

@function_tool
def creative_Writer(name: str) -> str:

    return f"Greeting, {name}! May your day be filled with inspiration and creativity"

planning_agent : Agent = Agent(
    name= "planningAgent",
    instructions= "you are a planning assistant. look at user request and use scientific resoning to plan the next steps.In response always include the scientific principles you used to plan",
    model= llm_model
)

# @function_tool
# def current_date() -> str:
#     return datetime.now().strftime("%Y-%m-%d")

orchestrator_agent : Agent = Agent(
    name= "DeepAgent",
    instructions="helpful agent that can questions and for planning work delegate to planning agent,",
    model= llm_model,
    tools=[],
    handoffs=[planning_agent]
)
res = Runner.run_sync(orchestrator_agent,"Do Deep search lead Generation system for a tax company in us?")
print("\n LAST AGENT",res.last_agent.name)
print("\n FINAL OUTPUT",res.final_output)
