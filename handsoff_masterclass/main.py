import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, handoff, RunContextWrapper, HandoffInputData
from pydantic import BaseModel
from agents.extensions import handoff_filters
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
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

def summeriza_news_transfer(data: HandoffInputData) -> HandoffInputData:
    print("\n\n [HANDOFF] Summerizing news transfer...\n\n")

    summarized_Converstion = "Get Latest tech news."

    return HandoffInputData(
        input_history=summarized_Converstion,
        # pre_handoff_items=data.pre_handoff_items,
        # new_items=data.new_items,
        pre_handoff_items=(),
        new_items=()
    )


def is_news_allowed(ctx : RunContextWrapper, agent : Agent) -> bool:
    return True if ctx.context.get("is_admin",False) else False
    False

@function_tool
def get_weather(city: str) -> str:
    """A simple function to get the weather for a user."""
    return f"The weather for {city} is sunny."


news_agent: Agent = Agent(
    name="NewsAgent",
    instructions="You get latest news about tech community and share it with me. Always transfer back to WeatherAgent after answering the question",
    model=llm_model,
    # tools=[get_weather],
    handoff_description="Expert News Updates about tech and all"
)

weather_agent: Agent = Agent(
    name="WeatherAgent",
    instructions=f"You are weather expert - share weather updates as I travel a lot. For all tech and news let the newsagent handle that part by delegation. {RECOMMENDED_PROMPT_PREFIX}",
    model=llm_model,
    # tools=[get_weather],
    # handoffs=[news_agent], 
    # handoffs=[handoff(agent=news_agent,input_filter=summeriza_news_transfer )]
    # handoffs=[handoff(agent=news_agent,is_enabled=False)],
    # handoffs=[handoff(agent=news_agent,is_enabled=True)],
    handoffs=[handoff(agent=news_agent,is_enabled=is_news_allowed)],
    
)
# news_agent.handoffs=[weather_agent]

res = Runner.run_sync(weather_agent, "Check if there's any news about openai after GPT-5 Launch, also what's the weather?",context={"is_admin": True})
print("\n Agent Name :",res.last_agent.name)
print("\n Agent Response :",res.final_output)

