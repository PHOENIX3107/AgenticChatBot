from openai.types import eval_stored_completions_data_source_config
from langgraphagenticai.state.state import State



class ChatbotWithToolNode:
    """
    chatbot logic enhanced with tool integration.
    """
    def __init__(self,model):
        self.llm=model
    def process(self,state:State)->dict:
        """
        processes the input state and generates a response with tool integration.

        """
        user_input=state["message"][-1] if state["messages"] else ""
        llm_response=self.llm.invoke([{"role":"user","content":user_input}])
        
        ## simulate tool-specific logic
        tools_response= f"Tool integration for: '{user_input}'"
        return{"messages":[llm_response,tools_response]}  

    def create_chatbot(self, tools):
        """
        Returns a chatbot node function.
        """

        llm_with_tools = self.llm.bind_tools(tools)
        def chatbot_node(state: State):
            """
            Chatbot logic for processing the input state and returning a response.
            """
            return {
            "messages": [llm_with_tools.invoke(state["messages"])]}
        return chatbot_node
        