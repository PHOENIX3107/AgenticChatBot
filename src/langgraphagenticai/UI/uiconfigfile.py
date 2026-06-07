import os
import configparser

class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        # Look for the ini file in the same directory as this file
        ini_path = os.path.join(os.path.dirname(__file__), "uiconfigfile.ini")
        if os.path.exists(ini_path):
            self.config.read(ini_path)

    def get_page_title(self):
        return self.config.get("DEFAULT", "PAGE_TITLE", fallback="Agentic Chat Bot")

    def get_llm_options(self):
        val = self.config.get("LLM_CONFIG", "LLM_OPTIONS", fallback="OpenAI,Groq,Google Gemini,Llama")
        return [item.strip() for item in val.split(",") if item.strip()]

    def get_use_case_options(self):
        val = self.config.get("USE_CASES", "USECASE_OPTIONS", fallback="Basic Chatbot,Chatbot woth Tool,AI News,Blog Generator")
        return [item.strip() for item in val.split(",") if item.strip()]

    def get_openai_model_options(self):
        val = self.config.get("LLM_CONFIG", "OPENAI_MODELS", fallback="gpt-4o,gpt-4-turbo,gpt-3.5-turbo")
        return [item.strip() for item in val.split(",") if item.strip()]

    def get_groq_model_options(self):
        val = self.config.get("LLM_CONFIG", "GROQ_MODELS", fallback="llama3-8b-8192,llama3-70b-8192,mixtral-8x7b-32768")
        return [item.strip() for item in val.split(",") if item.strip()]