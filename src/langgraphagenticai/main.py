import streamlit as st
from langgraphagenticai.UI.Streamlitui.loadui import LoadStreamlitUI
from langgraphagenticai.LLMs.groqllm import GroqLLM
from langgraphagenticai.LLMs.openaillm import OpenAI_LLM
from langgraphagenticai.graph.graph_builder import GraphBuilder
from langgraphagenticai.UI.Streamlitui.display_result import DisplayResultStreamlit

def load_langgraph_agenticai_app():
    """
    Loads and runs the LangGraph agenticai application with streamlit UI.
    This function initializes the UI and handles the user input, configures the LLM Model,
    sets up the graph based on the selected use case, and displays the output while
    implementing exception handling for robustness.
    """

    # Load UI
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()

    if not user_input:
        st.error("Error: failed to load user input from the UI")
        return
    user_message= st.chat_input("Type your message here")
    
    if user_message:
     try:

        selected_llm = user_input.get("Selected_llm")

        if selected_llm == "Groq":
            obj_llm_config = GroqLLM(
                user_controls_input=user_input
            )

        elif selected_llm == "OpenAI":
            obj_llm_config = OpenAI_LLM(
                user_controls_input=user_input
            )

        else:
            st.error(f"Unsupported LLM: {selected_llm}")
            return

        model = obj_llm_config.get_llm_model()

        if not model:
            st.error("Failed to initialize model")
            return

        usecase=user_input.get("Selected_usecase")
        if not usecase:
            st.error("Failed to load Use Case")
            return 
        ## graph builder

        graph_builder=GraphBuilder(model, user_input.get("TAVILY_API_KEY"))
        try:
            graph=graph_builder.setup_graph(usecase)
            
            DisplayResultStreamlit(usecase,graph,user_message).display_result_on_ui()
        except Exception as e:
            st.error(f"Error:Graph setup failed- {str(e)}")
            return

     except Exception as e:
        st.error(f"Error: {str(e)}")
        return
