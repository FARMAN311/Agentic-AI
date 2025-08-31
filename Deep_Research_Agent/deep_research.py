from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool, RunContextWrapper
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

web_search_agent: Agent = Agent(
    name="WebSearchAgent",
    instructions= "you are a web search assistance. Look at user request,plan and use web search to find relevent information",
    model=llm_model
)

reflective_agent: Agent = Agent(
    name="ReflectiveAgent",
    instructions="you are reflective assistant. look at user request and reflect on the best approch",
    model=llm_model
)
@function_tool
def current_date() -> str:
    return datetime.now().strftime("%Y-%m-%d")

def dynamic_instructions(context:RunContextWrapper, agent:Agent) -> str:
    prompt = f"""
    you are an orchestrator assistant.You manage specialized Agents to help users.
      your main goal is deep search for each user query.

      we follow a structured process for each deep search request.
      1. get current date
      2. do planning
      3. spawn multiple web search agents
      4. perform reflection to decide if deep goal is achieved

      finally get reflection to know if the task is achived. Current Date {current_date}
    """
    return prompt.format(dynamic_date=datetime.now().strftime("%Y-%m-%d"))
orchestrator_agent : Agent = Agent(
    name= "DeepAgent",
    instructions=dynamic_instructions,
    model= llm_model,
    tools=[current_date,
           planning_agent.as_tool(
                                  tool_name="planningAgent",
                                  tool_description="A planning agent that uses scientific reasoning to plan next steps"
                                  ),
                                  web_search_agent.as_tool(
                                      tool_name="webSearchAgent",
                                      tool_description="A Web Search Agent that find relevent information on the web"
                        
                                  ),
                                  reflective_agent.as_tool(
                                      tool_name="reflectiveAgent",
                                      tool_description="A reflective Agent that reflects on the best approach to take"
                                  )
                                  ]
)

res = Runner.run_sync(orchestrator_agent,"we have the software house do research on the best skill in ai Era which generate more revenue?")
print(res.final_output)

