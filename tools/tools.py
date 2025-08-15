from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_tavily import TavilySearch
from dotenv import load_dotenv

load_dotenv()

def get_profile_url_tavily(name: str):
    """Searches for Linkedin or Twitter Profile Page."""
    search = TavilySearchResults()
    res = search.invoke(f"{name}")
    return res[0]["url"]

