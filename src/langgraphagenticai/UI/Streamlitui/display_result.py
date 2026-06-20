
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage


class DisplayResultStreamlit:

    def __init__(self, usecase, graph, user_message, user_controls=None):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message
        self.user_controls = user_controls or {}

    def display_result_on_ui(self):

        usecase = self.usecase
        graph = self.graph
        user_message = self.user_message

        if usecase == "Basic Chatbot":

            for event in graph.stream(
                {"messages": ("user", user_message)}
            ):

                print(event.values())

                for value in event.values():

                    print(value["messages"])

                    with st.chat_message("user"):
                        st.write(user_message)

                    with st.chat_message("assistant"):
                        st.write(value["messages"].content)
        elif usecase in ("Chatbot with Tool", "Chatbot woth Tool"):
            initial_state = {
                "messages": [HumanMessage(content=user_message)]
            }

            res = graph.invoke(initial_state)

            for message in res["messages"]:
                if type(message) == HumanMessage:
                    with st.chat_message("user"):
                        st.write(message.content)

                elif type(message) == ToolMessage:
                    with st.chat_message("ai"):
                        st.write("Tool Call Start")
                        st.write(message.content)
                        st.write("Tool Call End")

                elif type(message) == AIMessage and message.content:
                    with st.chat_message("assistant"):
                        st.write(message.content)

        elif usecase == "AI News":
            frequency = str(self.user_controls.get("Time_Frame", "")).strip().lower()
            topic = str(
                self.user_controls.get("News_Topic")
                or st.session_state.get("news_topic")
                or "Artificial Intelligence"
            ).strip()
            article_count = self.user_controls.get("No_Of_Articles", 5)

            if not frequency:
                st.error("Please select a time frame for AI News.")
                return

            with st.spinner("Fetching and summarizing news...⌛"):
                result = graph.invoke(
                    {
                        "messages": [HumanMessage(content=frequency)],
                        "topic": topic,
                        "article_count": article_count,
                    }
                )

                try:
                    markdown_content = result.get("summary", "")

                    if markdown_content:
                        st.markdown(markdown_content, unsafe_allow_html=True)
                        return

                    ai_news_path = result.get("filename", f"./AINews/{frequency}_summary.md")
                    with open(ai_news_path, "r", encoding="utf-8") as file:
                        st.markdown(file.read(), unsafe_allow_html=True)

                except FileNotFoundError:
                    st.error(f"News Not Generated or File not found: {ai_news_path}")

                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        elif usecase == "Blog Generator":

            topic = self.user_controls.get("Blog_Topic", "")
            tone = self.user_controls.get("Blog_Tone", "Professional")
            length = self.user_controls.get("Blog_Length", "Medium")
            language = self.user_controls.get("Language", "English")

            if not topic:
                st.error("Please enter a blog topic.")
                return

            with st.spinner("Generating blog...✍️"):

                result = graph.invoke(
                    {
                        "topic": topic,
                        "language": language,
                        "current_language": language
                    }
                )

                try:
                    blog = result.get("blog")

                    if not blog:
                        st.error("Blog generation failed.")
                        return

                    if isinstance(blog, dict):
                        title = blog.get("title", "")
                        content = blog.get("content", "")
                    else:
                        title = getattr(blog, "title", "")
                        content = getattr(blog, "content", "")

                    st.markdown(f"# {title}")

                    st.caption(f"Language: {language}")

                    st.divider()

                    st.markdown(content)

                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
