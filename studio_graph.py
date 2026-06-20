import os
from langchain_openai import ChatOpenAI
from langgraphagenticai.graph.graph_builder import GraphBuilder
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o",
    api_key=os.getenv("OPENAI_API_KEY")
)

graph = GraphBuilder(
    llm,
    tavily_api_key=os.getenv("TAVILY_API_KEY")
).blog_generator_build_graph().compile()