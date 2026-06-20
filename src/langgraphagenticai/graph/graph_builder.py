from langgraph.graph import StateGraph, START, END
from langgraphagenticai.state.state import State
from langgraphagenticai.nodes.basicchatbot_node import BasicChatbotNode
from langgraphagenticai.tools.search_tool import get_tools, create_tool_node
from langgraph.prebuilt import tools_condition
from langgraphagenticai.nodes.chatbot_with_tool_node import ChatbotWithToolNode
import os
from langgraphagenticai.nodes.ai_news_node import AiNewsNode
from  langgraphagenticai.state.blogstate import BlogState
from langgraphagenticai.nodes.blog_node import BlogNode

CHATBOT_WITH_TOOL_USECASES = {"Chatbot with Tool", "Chatbot woth Tool"}


class GraphBuilder:
    def __init__(self, model, tavily_api_key=None):
        self.llm = model
        self.tavily_api_key = tavily_api_key
        if tavily_api_key:
            os.environ["TAVILY_API_KEY"] = tavily_api_key
        self.graph_builder = StateGraph(State)

    def _reset_graph_builder(self):
        self.graph_builder = StateGraph(State)

    def setup_graph(self, usecase):
        """
        Build and compile the graph for the requested use case.
        """
        usecase = (usecase or "").strip()

        if usecase == "Basic Chatbot":
            self._reset_graph_builder()
            self.basic_chatbot_build_graph()
            return self.graph_builder.compile()

        if usecase in CHATBOT_WITH_TOOL_USECASES:
            self._reset_graph_builder()
            self.chatbot_with_tool_build_graph()
            return self.graph_builder.compile()

        if usecase == "AI News":
            self._reset_graph_builder()
            self.ai_news_build_graph()
            return self.graph_builder.compile()

        if usecase == "Blog Generator":
            return self.blog_generator_build_graph().compile()

        raise ValueError(f"Unsupported use case: {usecase}")
    
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

    def ai_news_build_graph(self):
        """
        Builds a graph for AI News aggregation and summarization.
        """
        if not self.tavily_api_key:
            raise ValueError("Tavily API Key is required for AI News")

        ai_news_node = AiNewsNode(self.llm)

        self.graph_builder.add_node("fetch_news", ai_news_node.fetch_news)
        self.graph_builder.add_node("summarize_news", ai_news_node.summarize_news)
        self.graph_builder.add_node("save_result", ai_news_node.save_result)

        self.graph_builder.add_edge(START, "fetch_news")
        self.graph_builder.add_edge("fetch_news", "summarize_news")
        self.graph_builder.add_edge("summarize_news", "save_result")
        self.graph_builder.add_edge("save_result", END)


    ### BLOG
    def blog_generator_build_graph(self):
        """
        Builds a graph to generate blogs based on the topic.
        """
        self.graph_builder = StateGraph(BlogState)
        self.blog_node_obj = BlogNode(self.llm)
        self.graph_builder.add_node(
            "title_creation",
            self.blog_node_obj.title_creation
        )
        self.graph_builder.add_node(
            "content_creation",
            self.blog_node_obj.content_genration
        )
        self.graph_builder.add_node(
            "hindi_translation",
            self.blog_node_obj.hindi_translation
        )
        self.graph_builder.add_node(
            "french_translation",
            self.blog_node_obj.french_translation
        )
        self.graph_builder.add_node(
            "route",
            self.blog_node_obj.route
        )

        self.graph_builder.add_edge(
            START,
            "title_creation"
        )
        self.graph_builder.add_edge(
            "title_creation",
            "content_creation"
        )
        self.graph_builder.add_edge(
            "content_creation",
            "route"
        )
        self.graph_builder.add_conditional_edges(
            "route",
            self.blog_node_obj.route_decision,
            {
                "Hindi": "hindi_translation",
                "French": "french_translation",
                "English": END
            }
        )
        self.graph_builder.add_edge(
            "hindi_translation",
            END
        )
        self.graph_builder.add_edge(
            "french_translation",
            END
        )
        return self.graph_builder

    




