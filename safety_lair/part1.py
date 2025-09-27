import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool
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

@function_tool
def get_weather(city: str) -> str:
    """A simple function to get the weather for a user."""
    return f"The weather for {city} is sunny. And Current Temperature is 25'C. Humidity is 60% and wind speed is 15 km/hr, sourse 201-p002 section agents"

class ExtraWeatherInfo(BaseModel):
    humidity: str | None = Field(default=None, description="Humedity level")
    wind_speed: str | None = Field(default=None, description="Wind Speed")
    source : list[str] | None = Field(default=None, description="Source of the weather data")

class WeatherData(BaseModel):
    location : str | None = Field(default=None, description="This is the location")
    tamperature : str | None = Field(default=None, description="This is the Tamperature")
    notes : str | None = Field(default=None, description="any additional notes about  ")
    extra_data : ExtraWeatherInfo | None = Field(default=None, description="Any extra data")
    

base_agent: Agent = Agent(
    name="WeatherAgent",
    instructions="You are a helpful assistant.",
    # model=llm_model,
    tools=[get_weather],
    output_type=WeatherData
)


res = Runner.run_sync(base_agent, "What's the weather in Karachi?")
print(res.final_output)
# print("\n [LOCATION:]", res.final_output.location)
# print("\n [TEMP :]", res.final_output.tamperature)
# print("\n [INFO :]", res.final_output.extra_info)

# Now check the trace in 