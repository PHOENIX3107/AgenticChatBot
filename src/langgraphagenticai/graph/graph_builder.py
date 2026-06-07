from langgraph.graph import StateGraph
from langgraphagenticai.state.state import State 
from langgraph.graph import StateGraph,START,END
from langgraphagenticai.nodes.basicchatbot_node import BasicChatbotNode
class GraphBuilder:
    def __init__(self,model):
        self.llm=model
        self.graph_builder=StateGraph(State)
    
    def basic_chatbot_build_graph(self):
        """
        Builds a basic chatbot graph using langgraph.
        this  method initializes a chatbot node using the 'BasicChatbotNode' class.
        and integrates it into the graph. The chatbot node is set as both the entry 
        and exist point of the graph.

        """

        self.basic_chatbot_node=BasicChatbotNode(self.llm)  

        self.graph_builder.add_node("chatbot",self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_edge("chatbot",END)
    def setup_graph(self, usecase: str):

     if usecase == "Basic Chatbot":

        self.basic_chatbot_build_graph()

     else:
        raise ValueError(f"Unsupported use case: {usecase}")

     return self.graph_builder.compile()
            

    