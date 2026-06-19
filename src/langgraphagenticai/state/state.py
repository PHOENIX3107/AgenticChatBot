from typing import Annotated
from typing_extensions import NotRequired, TypedDict

from langgraph.graph.message import add_messages

class State(TypedDict):
    """
    Represent the structure of the state used in the graph.
    """
    messages: Annotated[list, add_messages]
    frequency: NotRequired[str]
    topic: NotRequired[str]
    article_count: NotRequired[int]
    news_data: NotRequired[list]
    summary: NotRequired[str]
    filename: NotRequired[str]
