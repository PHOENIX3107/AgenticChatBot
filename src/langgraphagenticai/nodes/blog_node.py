from langchain_core.messages import HumanMessage
from langgraphagenticai.state.blogstate import BlogState
from langgraphagenticai.state.blogstate import Blog


class Blognode:
    """
    A class to represent the blog node
    """
    def __init__(self,llm):
        self.llm = llm
        
    def title_creation(self,state:BlogState):
        """
        Creates title for the blog
        """
        if "topic" in state and state["topic"]:
            prompt="""
                        You are an expert in blog title generation. Your task is to create a compelling and creative title for a blog based on the given {topic}.
                        this title must be related to the {topic} and must be engaging and interesting and should be SEO friendly.
            
                        """
            system_message=prompt.format(topic=state['topic'])
            response=self.llm.invoke(system_message)
            return {"blog":{"title":response.content}}
            
    def content_genration(self,state:BlogState):
        if "topic" in state and state["topic"]:
            system_prompt = """
            You are expert blog writer.
            Use Markdown formatting.
            Generate a blog content for the {topic} making sure its detailed and most professionaly written 
            """
    
            system_message = system_prompt.format(
                topic=state["topic"]
            )

            response = self.llm.invoke(system_message)

            return {
                "blog": {
                    "title": state["blog"]["title"],
                    "content": response.content
                }
            }
    def translation(self,state:BlogState):
        """
        Translate the content to the specified language
        """
        translation_prompt="""
        Translate the following content into {current_language}.
        Respond only in {current_language}.
        - Maintain the original tone, style and formatting.
        - Adapt cultural references and idioms to be appropriate for {current_language}.

        ORIGINAL CONTENT:
        {blog_content}
        """

        blog_content = state["blog"]["content"]
        message=[
            HumanMessage(translation_prompt.format(current_language=state["current_language"],blog_content=blog_content))
        ]
        translation_content = self.llm.with_structured_output(Blog).invoke(message)

        return {
            "blog": translation_content
        }
    def hindi_translation(self, state: BlogState):

        state["current_language"] = "Hindi"

        return self.translation(state)

    def french_translation(self, state: BlogState):

        state["current_language"] = "French"

        return self.translation(state)
        
    def route(self, state: BlogState):

        return state


    def route_decision(self, state: BlogState):

        language = str(state.get("language", "English")).strip().lower()

        if language == "hindi":

            return "Hindi"

        elif language == "french":

            return "French"

        return "English"

BlogNode = Blognode
