import os
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool, ModelSettings
from dotenv import load_dotenv, find_dotenv
from tavily import TavilyClient

load_dotenv(find_dotenv())
set_tracing_disabled(disabled=True)
gemini_api_key = os.environ.get("GEMINI_API_KEY")
tavily_api_key = os.environ.get("TAVILY_API_KEY")

tavily_client = TavilyClient(api_key=tavily_api_key)

Provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

llm_model = OpenAIChatCompletionsModel(
    openai_client=Provider,
    model="gemini-2.5-flash"
)

@function_tool()
def search(query : str) -> str:
    print("[Tools....] search for: ", query)
    response = tavily_client.search(query)
    return response
@function_tool()
def extract_content(urls: list) -> dict:
    print("[tool...] Extracting content from urls: ",urls)
    response = tavily_client.extract(urls)
    #print("[Tool....] Extraction Completed.", response)
    return response

agent : Agent = Agent(
    name = "Search Agent",
    model= llm_model,
    tools=[search, extract_content],
    instructions="you are deep search agent. Use the tools provided to answer the questions.Always use the search tools first to find relevent information, then use the extract tools to get the details content from the urls returned",
    model_settings=ModelSettings(temperature=1.9,tool_choice="auto", max_tokens=1000)
)
# print("agent.tools",agent.tools)
runner = Runner.run_sync(agent,"Research on the impact of Agentic AI fro white Collar jobs")

print(runner.final_output)