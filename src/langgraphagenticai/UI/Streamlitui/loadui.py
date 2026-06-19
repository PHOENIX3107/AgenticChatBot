import streamlit as st

from langgraphagenticai.UI.uiconfigfile import Config


AGENTIC_LOGO = """
╔══════════════════════════════╗
║  🤖 AGENTIC CHAT BOT ⚡      ║
╚══════════════════════════════╝
"""


class LoadStreamlitUI:

    def __init__(self):
        self.config = Config()
        self.user_controls = {}

    def load_streamlit_ui(self):

        st.set_page_config(
            page_title=f"🤖 {self.config.get_page_title()}",
            page_icon="⚡",
            layout="wide",
            initial_sidebar_state="expanded"
        )

        with st.sidebar:

            st.code(AGENTIC_LOGO)
            st.divider()

            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_use_case_options()

            # ---------------- LLM SELECTION ---------------- #

            self.user_controls["Selected_llm"] = st.selectbox(
                "Select LLM",
                llm_options
            )

            # OpenAI
            if self.user_controls["Selected_llm"] == "OpenAI":

                model_options = self.config.get_openai_model_options()

                self.user_controls["Selected_model"] = st.selectbox(
                    "Select OpenAI Model",
                    model_options
                )

                self.user_controls["OPENAI_API_KEY"] = st.text_input(
                    "Enter OpenAI API Key",
                    type="password"
                )

                if not self.user_controls["OPENAI_API_KEY"]:
                    st.warning("Please enter OpenAI API Key")

            # Groq
            elif self.user_controls["Selected_llm"] == "Groq":

                model_options = self.config.get_groq_model_options()

                self.user_controls["Selected_model"] = st.selectbox(
                    "Select Groq Model",
                    model_options
                )

                self.user_controls["GROQ_API_KEY"] = st.text_input(
                    "Enter Groq API Key",
                    type="password"
                )

                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning("Please enter Groq API Key")

            # Gemini
            elif self.user_controls["Selected_llm"] == "Google Gemini":

                self.user_controls["GEMINI_API_KEY"] = st.text_input(
                    "Enter Gemini API Key",
                    type="password"
                )

                if not self.user_controls["GEMINI_API_KEY"]:
                    st.warning("Please enter Gemini API Key")

            # Llama
            elif self.user_controls["Selected_llm"] == "Llama":

                st.info("Configure Llama model locally.")

            st.divider()

            # ---------------- USE CASE ---------------- #

            self.user_controls["Selected_usecase"] = st.selectbox(
                "Select Use Case",
                usecase_options
            )

            # Basic Chatbot
            if self.user_controls["Selected_usecase"] == "Basic Chatbot":

                self.user_controls["System_Prompt"] = st.text_area(
                    "System Prompt",
                    value="You are a helpful AI assistant."
                )

            # Chatbot with Tool
            elif self.user_controls["Selected_usecase"] in ("Chatbot with Tool", "Chatbot woth Tool"):

                self.user_controls["TAVILY_API_KEY"] = st.session_state["TAVILY_API_KEY"] = st.text_input(
                    "Enter Tavily API Key",
                    type="password"
                )
                if not self.user_controls["TAVILY_API_KEY"]:
                    st.warning("Please enter Tavily API Key")

                self.user_controls["System_Prompt"] = st.text_area(
                    "System Prompt",
                    value="You are an AI assistant with access to tools."
                )

                self.user_controls["Enable_Web_Search"] = st.checkbox(
                    "Enable Web Search",
                    value=True
                )

            # AI News
            elif self.user_controls["Selected_usecase"] == "AI News":
                self.user_controls["TAVILY_API_KEY"] = st.session_state["TAVILY_API_KEY"] = st.text_input(
                    "Enter Tavily API Key",
                    type="password"
                )
                if not self.user_controls["TAVILY_API_KEY"]:
                    st.warning("Please enter Tavily API Key")

                st.subheader("AI News Explorer")

                self.user_controls["News_Topic"] = st.text_input(
                    "News Topic",
                    value="Artificial Intelligence",
                    placeholder="AI, robotics, OpenAI, Nvidia"
                )

                self.user_controls["Time_Frame"] = st.selectbox(
                    "Select Time Frame",
                    ["Daily", "Weekly", "Monthly"],
                    index=0
                )

                self.user_controls["No_Of_Articles"] = st.slider(
                    "Number of Articles",
                    min_value=1,
                    max_value=10,
                    value=5
                )

                self.user_controls["Fetch_News"] = st.button("Fetch Latest AI News", use_container_width=True)

                if self.user_controls["Fetch_News"]:
                    st.session_state["news_topic"] = self.user_controls["News_Topic"]
                    st.session_state["timeframe"] = self.user_controls["Time_Frame"]


            # Blog Generator
            elif self.user_controls["Selected_usecase"] == "Blog Generator":

                self.user_controls["Blog_Topic"] = st.text_input(
                    "Blog Topic",
                    placeholder="Future of Agentic AI"
                )

                self.user_controls["Blog_Length"] = st.selectbox(
                    "Blog Length",
                    ["Short", "Medium", "Long"]
                )

                self.user_controls["Blog_Tone"] = st.selectbox(
                    "Writing Tone",
                    [
                        "Professional",
                        "Technical",
                        "Casual",
                        "Educational"
                    ]
                )

            st.divider()

            self.user_controls["Run"] = st.button(
                "🚀 Run Agent",
                use_container_width=True
            )

        # ---------------- MAIN PAGE ---------------- #

        st.title(self.config.get_page_title())

        st.caption(
            "Build Stateful Agentic AI Applications with LangGraph"
        )

        st.divider()

        return self.user_controls
