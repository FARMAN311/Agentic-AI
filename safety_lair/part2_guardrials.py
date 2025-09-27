import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, GuardrailFunctionOutput, input_guardrail, InputGuardrailTripwireTriggered, RunContextWrapper
from pydantic import BaseModel, Field
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

@input_guardrail
def input_weather_Checker(ctx: RunContextWrapper,agent: Agent,input):
    print("\n [Agent]",agent.name)
    print("\n [INPUT]",input)
    print("\n [CONTEXT]",ctx)

    return GuardrailFunctionOutput(
        output_info="passed",
        # tripwire_triggered=True,
        tripwire_triggered=False
                                   )
 

base_agent: Agent = Agent(
    name="WeatherAgent",
    instructions="You are a helpful assistant.",
    model=llm_model,
    input_guardrails=[input_weather_Checker]
)

try:
    # res = Runner.run_sync(base_agent, "What's the weather in Karachi?")
    res = Runner.run_sync(base_agent, [{"Role":"User","Content":"What's The Weather like in SF?"}])
    print("[output]",res.to_input_list())
except InputGuardrailTripwireTriggered as e:
    print("Alert: Guardrails tripwire was triggered")