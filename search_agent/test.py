import os
from tavily import TavilyClient
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

tavily_api_key = os.environ.get("TAVILY_API_KEY")
tavily_client = TavilyClient(api_key=tavily_api_key)

reponse = tavily_client.search("Agentic AI")
print("[Tool....] Search Completed.", reponse)