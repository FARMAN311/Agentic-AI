from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool
import os
import asyncio
from dotenv import load_dotenv, find_dotenv
from dataclasses import dataclass
from typing import Callable
import time
from openai.types.responses import ResponseTextDeltaEvent

load_dotenv(find_dotenv())

gemini_api_key : str | None = os.environ.get("GEMINI_API_KEY")
set_tracing_disabled(disabled=True)

external_client: AsyncOpenAI = AsyncOpenAI(api_key=gemini_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client)
@function_tool
def greet(name: str) -> str:

    return f"hello, {name}!"

@function_tool
def creative_Writer(name: str) -> str:

    return f"Greeting, {name}! May your day be filled with inspiration and creativity"

base_agent: Agent = Agent(
    name= "baseagent",
    instructions="you are a helpful assistant.",
    model= llm_model,
    tools=[greet]
)
 
empathic_lead_generation_agent: Agent = base_agent.clone(
    instructions = "you are an emphathic lead generation assistant."
)
create_agent: Agent = base_agent.clone(
    # name = "createagent",
    instructions = "you are a creative assistant.",
    tools = base_agent.tools.copy()
)
create_agent.tools.append(creative_Writer)
print(f"Base Agent: {base_agent.name}, Tools: {[tool.name for tool in base_agent.tools]}")
print(f"create_agent: {create_agent.name}, Tools: {[tool.name for tool in create_agent.tools]}")

# print(f"base_agent: {base_agent.name}, instructions : {base_agent.instructions}")
# print(f"create_agent: {create_agent.name}, instructions : {create_agent.instructions}")

# create_agent.name="CreativeAgent"
# print(f"update create_agent: {create_agent.name}, instructions : {create_agent.instructions}")
# print(f"base_agent after Update: {base_agent.name}, instructions : {base_agent.instructions}")