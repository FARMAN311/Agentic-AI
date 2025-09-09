import os
import asyncio
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, MaxTurnsExceeded, ModelSettings, RunContextWrapper
from agents.agent import StopAtTools
from dataclasses import dataclass
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

@dataclass
class UserScope:
    is_admin:bool

# def is_weather_allowed(context, agent) -> bool:
#     print("Is Allowed")
#     return True


# async def is_weather_allowed(ctx:RunContextWrapper, agent:Agent) -> bool:
#     print("Check if weather is Allowed...",ctx.context)
#     return False

async def is_weather_allowed(ctx:RunContextWrapper[UserScope], agent:Agent[UserScope]) -> bool:
    print("Check if weather is Allowed...",ctx.context)
    return True if ctx.context.is_admin else False


# @function_tool(name_override="weather_calling_tool")
# @function_tool(is_enabled=True)
# @function_tool(is_enabled=False)
@function_tool(is_enabled=is_weather_allowed)
def get_weather(city: str) -> str:
    """A simple function to get the weather for a user."""
    return f"sunny."

base_agent: Agent = Agent(
    name="WeatherAgent",
    # instructions="You are a helpful assistant. if some tools is not available - call it at least 5 times before giving up",
    model=llm_model,
    tools=[get_weather],
    # model_settings=ModelSettings(tool_choice="none")
    # tool_use_behavior="stop_on_first_tool"
    # tool_use_behavior="run_llm_again"
    # tool_use_behavior=StopAtTools(stop_at_tool_names=["get_travel_plan"])
)
# try:
#     res = Runner.run_sync(base_agent, "What is weather in karachi", max_turns=3)
#     print(res.final_output)
# except MaxTurnsExceeded as e:
#     print(f"Max turn exceeded: {e}")
async def main():
    # abdul_scope = UserScope(is_admin=True)
    abdul_scope = UserScope(is_admin=False)
    res = await Runner.run(base_agent, "What is weather in karachi", context=abdul_scope)
    print(res.final_output)

if __name__ =="__main__":
    asyncio.run(main())