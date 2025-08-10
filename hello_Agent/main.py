import os
from typing import Union, Optional
import asyncio
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, AsyncOpenAI, set_tracing_disabled, set_default_openai_client,set_default_openai_key, set_default_openai_api, function_tool
from agents.run import RunConfig
_: bool = load_dotenv(find_dotenv())
set_default_openai_api("chat_completions")
gemini_api_key : str | None = os.environ.get("GEMINI_API_KEY")
print("gemini Api key is :",gemini_api_key)
# Tracing Disabled
set_tracing_disabled(disabled=True)
# Which LLM Service?
external_client: AsyncOpenAI = AsyncOpenAI(
    api_key= gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
set_default_openai_client(external_client)
# Which LLM Model?
#llm_model : OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
#    model= "gemini-2.5-flash",
#   openai_client=external_client
#)
#config = RunConfig(
#   model=llm_model,
#   model_provider=external_client,
#   tracing_disabled=True
#)
@function_tool
def add(a: int, b:int) -> int:
    print(f"\n\nAdding {a} and {b}\n\n")
    return a + b
@function_tool
def Subtract(a: int, b:int) -> int:
    print(f"\n\nSubtracting {a} and {b}\n\n")
    return a - b 
math_agent : Agent = Agent(
    name="Alex - The Math Genious",
    model="gemini-2.0-flash",
    #tools=[add,Subtract]
)
async def call_agent():
    output = await Runner.run(starting_agent=math_agent,input="What is 2 + 2?")
    print(output.final_output)

asyncio.run(call_agent())