import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool
from agents.agent import StopAtTools
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
    """A simple function to get the weather for a user."""
    return f"sunny."
@function_tool
def get_travel_plan(city: str) -> str:
    return f"Travel Plan is not available"

base_agent: Agent = Agent(
    name="WeatherAgent",
    instructions="You are a helpful assistant.",
    model=llm_model,
    tools=[get_weather,get_travel_plan],
    # tool_use_behavior="stop_on_first_tool",
    # tool_use_behavior="run_llm_again"
    tool_use_behavior=StopAtTools(stop_at_tool_names=["get_travel_plan"])
)

res = Runner.run_sync(base_agent, "make me travel plan for karachi?")
print(res.final_output)

# Now check the trace in 