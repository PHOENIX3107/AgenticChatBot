from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from langgraph.prebuilt import ToolNode



def get_tools(tavily_api_key=None):
    """
    Returns the list of tools to be used by the chatbot.
    """
    api_wrapper = TavilySearchAPIWrapper(tavily_api_key=tavily_api_key)
    tools=[TavilySearchResults(max_results=2, api_wrapper=api_wrapper)]
    return tools

def create_tool_node(tools):
    """
    creates and returns a tool node for the graph
    """
    return ToolNode(tools=tools)
    
