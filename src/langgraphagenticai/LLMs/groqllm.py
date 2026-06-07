import os
import streamlit as st
from langchain_groq import ChatGroq

class GroqLLM:
    def __init__(self, user_controls_input):
        self.user_controls_input = user_controls_input

    def get_llm_model(self):
        try:
            # Safely get key from user_controls_input dictionary
            groq_api_key = self.user_controls_input.get('GROQ_API_KEY', '').strip()
            selected_groq_model = self.user_controls_input.get('Selected_model')

            # Fallback to environment variable if not provided in UI
            if not groq_api_key:
                groq_api_key = os.environ.get("GROQ_API_KEY", "").strip()

            if not groq_api_key:
                st.error("Please provide Groq API Key")
                return None
            
            # Corrected 'temparature' spelling to 'temperature'
            llm = ChatGroq(api_key=groq_api_key, model=selected_groq_model, temperature=0.7)

        except Exception as e:
            raise ValueError(f"Error in initializing Groq LLM: {str(e)}")
        return llm
