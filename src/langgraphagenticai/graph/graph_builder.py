from langgraph.graph import StateGraph, START, END
from langgraphagenticai.state.state import State
from langgraphagenticai.nodes.basicchatbot_node import BasicChatbotNode
from langgraphagenticai.tools.search_tool import get_tools, create_tool_node
from langgraph.prebuilt import tools_condition
from langgraphagenticai.nodes.chatbot_with_tool_node import ChatbotWithToolNode


CHATBOT_WITH_TOOL_USECASES = {"Chatbot with Tool", "Chatbot woth Tool"}


class GraphBuilder:
    def __init__(self, model, tavily_api_key=None):
        self.llm = model
        self.tavily_api_key = tavily_api_key
        self.graph_builder = StateGraph(State)
    
    def basic_chatbot_build_graph(self):
        """
        Builds a basic chatbot graph using langgraph.
        this  method initializes a chatbot node using the 'BasicChatbotNode' class.
        and integrates it into the graph. The chatbot node is set as both the entry 
        and exist point of the graph.

        """
        self.basic_chatbot_node = BasicChatbotNode(self.llm)

        self.graph_builder.add_node("chatbot", self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot", END)

    def chatbot_with_tool_build_graph(self):
        """
        Builds an advanced chatbot graph with tool integration.
        """
        if not self.tavily_api_key:
            raise ValueError("Tavily API Key is required for Chatbot with Tool")

        tools = get_tools(self.tavily_api_key)
        tool_node = create_tool_node(tools)
        chatbot_node = ChatbotWithToolNode(self.llm).create_chatbot(tools)

        self.graph_builder.add_node("chatbot", chatbot_node)
        self.graph_builder.add_node("tools", tool_node)
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_conditional_edges("chatbot", tools_condition)
        self.graph_builder.add_edge("tools", "chatbot")

    def setup_graph(self, usecase: str):
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()
        elif usecase in CHATBOT_WITH_TOOL_USECASES:
            self.chatbot_with_tool_build_graph()
        else:
            raise ValueError(f"Unsupported use case: {usecase}")

        return self.graph_builder.compile()
