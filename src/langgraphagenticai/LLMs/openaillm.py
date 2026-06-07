import os
import streamlit as st
from langchain_openai import ChatOpenAI


class OpenAI_LLM:
    def __init__(self, user_controls_input):
        self.user_controls_input = user_controls_input

    def get_llm_model(self):
        try:
            # Safely get key from user_controls_input dictionary
            openai_api_key = self.user_controls_input.get('OPENAI_API_KEY', '').strip()
            selected_openai_model = self.user_controls_input.get('Selected_model')

            # Fallback to environment variable if not provided in UI
            if not openai_api_key:
                openai_api_key = os.environ.get("OPENAI_API_KEY", "").strip()

            if not openai_api_key:
                st.error("Please provide OpenAI API Key")
                return None
            
            # Corrected 'temparature' spelling to 'temperature'
            llm = ChatOpenAI(api_key=openai_api_key, model=selected_openai_model, temperature=0.7)

        except Exception as e:
            raise ValueError(f"Error in initializing OpenAI LLM: {str(e)}")
        return llm
