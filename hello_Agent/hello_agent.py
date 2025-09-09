import os
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool, ModelSettings
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
set_tracing_disabled(disabled=True)
gemini_api_key = os.environ.get("GEMINI_API_KEY")
tavily_api_key = os.environ.get("TAVILY_API_KEY")


Provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

llm_model = OpenAIChatCompletionsModel(
    openai_client=Provider,
    model="gemini-2.5-flash"
)

maths_agent : Agent = Agent(
    name="math_agent",
    instructions="""you are a helpul math assistant for k12""",
    model=llm_model
)

result : Runner = Runner.run_sync(maths_agent,"Why Learn maths for AI agents")
print("\n calling Agent \n")
print(result.final_output)