from langgraphagenticai.state.state import State

class BasicChatbotNode:
    """
    Basic Chatbot logic implementation
    """ 
   
    def __init__(self, model):
        self.llm = model

    def process(self, state: State) -> dict:
        """
        Process the input State and generate a chatbot response using the configured LLM.
        """
        return {"messages": self.llm.invoke(state["messages"])}
