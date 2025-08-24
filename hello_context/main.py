import os
import asyncio
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool, RunContextWrapper, ItemHelpers
from dataclasses import dataclass
from typing import Callable
import time
from openai.types.responses import ResponseTextDeltaEvent

_: bool = load_dotenv(find_dotenv())

gemini_api_key : str | None = os.environ.get("GEMINI_API_KEY")

set_tracing_disabled(disabled=True)

external_client: AsyncOpenAI = AsyncOpenAI(api_key=gemini_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client)

@dataclass
class UserContext:
    username: str
    email: str | None = None

@function_tool()
async def search(local_context: RunContextWrapper[UserContext], query: str) -> str:
    # print("\n\nSome Data\n\n", local_context.context.username)
    # print(f"Search for : {query}")
    time.sleep(2)
    return "NO result found. "

async def Special_prompt(spacial_context:RunContextWrapper[UserContext],agent)-> str:
    print(f"\nUser:{spacial_context.context},\n Agent: {agent.name}\n")
    return f"You are a math Expert. user:{spacial_context.context.username}, Agent : {agent.name}. please assist with math-related queries."
math_agent : Agent = Agent(name="Genious",instructions=Special_prompt,model=llm_model, tools=[search])

async def call_agent():
    User_Context = UserContext(username="abdullah")
    output = Runner.run_streamed(
        starting_agent=math_agent,
        input="hi",
        context=User_Context                      
        )
    async for event in output.stream_events():
        # print(output,"\n\n")
        if event.type == "raw_response_event":
            continue
            # print(event.data.delta, end="", flush=True)
    # print(output.final_output)

asyncio.run(call_agent())

