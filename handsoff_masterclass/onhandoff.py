import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, handoff, RunContextWrapper
from pydantic import BaseModel

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

class NewsRequest(BaseModel):
    topic : str
    Reason : str


@function_tool
def get_weather(city: str) -> str:
    """A simple function to get the weather for a user."""
    return f"The weather for {city} is sunny."

def on_news_transfer(ctx: RunContextWrapper, input_data:NewsRequest) -> None:
    print(f"\n Transfering to for news updates. input data : ",input_data,"\n")

news_agent: Agent = Agent(
    name="NewsAgent",
    instructions="You get latest news about tech community and share it with me.",
    model=llm_model,
    tools=[get_weather],
    handoff_description="Expert News Updates about tech and all"
)

weather_agent: Agent = Agent(
    name="WeatherAgent",
    instructions="You are weather expert - share weather updates as I travel a lot. For all tech and news let the newsagent handle that part by delegation",
    model=llm_model,
    tools=[get_weather],
    # handoffs=[news_agent], 
    handoffs=[handoff(agent=news_agent,on_handoff=on_news_transfer, input_type=NewsRequest)]
)

res = Runner.run_sync(weather_agent, "Check if there's any news about openai after GPT-5 Launch?")
print("\n Agent Name :",res.last_agent.name)
print("\n Agent Response :",res.final_output)

