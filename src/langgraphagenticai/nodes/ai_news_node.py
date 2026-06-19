from pathlib import Path
from typing import Any
import re

from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate

class AINewsNode:
    def __init__(self, llm, output_dir: str | Path = "AINews"):
        """
        Initialize the AI News node with the configured LLM and output path.
        """
        self.tavily = TavilyClient()
        self.llm = llm
        self.output_dir = Path(output_dir)

    @staticmethod
    def _extract_frequency(state: dict[str, Any]) -> str:
        """
        Resolve the requested time frame from the graph state.
        """
        frequency = state.get("frequency")
        if isinstance(frequency, str) and frequency.strip():
            return frequency.strip().lower()

        messages = state.get("messages", [])
        if isinstance(messages, str):
            return messages.strip().lower()

        if isinstance(messages, list) and messages:
            latest_message = messages[-1]
            content = getattr(latest_message, "content", None)
            if content:
                return str(content).strip().lower()
            if isinstance(latest_message, dict):
                return str(latest_message.get("content", "")).strip().lower()
            return str(latest_message).strip().lower()

        raise ValueError(
            "AI News requires a time frame such as Daily, Weekly, or Monthly."
        )

    @staticmethod
    def _extract_topic(state: dict[str, Any]) -> str:
        topic = state.get("topic")
        if isinstance(topic, str) and topic.strip():
            return topic.strip()
        return "Artificial Intelligence"

    @staticmethod
    def _extract_article_count(state: dict[str, Any]) -> int:
        article_count = state.get("article_count", 5)
        try:
            article_count = int(article_count)
        except (TypeError, ValueError):
            article_count = 5

        if article_count < 1:
            return 1
        if article_count > 10:
            return 10
        return article_count

    @staticmethod
    def _slugify(value: str) -> str:
        slug = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
        return slug or "topic"

    def fetch_news(self, state: dict[str, Any]) -> dict[str, Any]:
        """
        Fetch AI news based on the specified frequency.
        """
        frequency = self._extract_frequency(state)
        topic = self._extract_topic(state)
        article_count = self._extract_article_count(state)
        time_range_map = {"daily": "d", "weekly": "w", "monthly": "m", "year": "y", "yearly": "y"}
        days_map = {"daily": 1, "weekly": 7, "monthly": 30, "year": 365, "yearly": 365}

        if frequency not in time_range_map:
            raise ValueError(
                f"Unsupported AI News frequency: {frequency}. "
                "Use daily, weekly, monthly, or yearly."
            )

        state["frequency"] = frequency
        state["topic"] = topic
        state["article_count"] = article_count

        response = self.tavily.search(
            query=f"latest {topic} news",
            topic="news",
            time_range=time_range_map[frequency],
            include_answer="advanced",
            max_results=article_count,
            days=days_map[frequency],
        )

        results = response.get("results", [])
        unique_results = []
        seen_urls = set()
        for item in results:
            url = item.get("url")
            key = url or item.get("title") or item.get("content")
            if key in seen_urls:
                continue
            seen_urls.add(key)
            unique_results.append(item)

        state["news_data"] = unique_results[:article_count]
        return state


    def summarize_news(self, state: dict[str, Any]) -> dict[str, Any]:
        """
        Summarize the fetched news using an LLM.
        """
        news_items = state.get("news_data", [])
        topic = state.get("topic", "Artificial Intelligence")

        prompt_template = ChatPromptTemplate.from_messages([
            (
                "system",
                f"""Summarize the provided news articles about {topic} into markdown format.
                Only use the supplied articles. Do not invent additional articles or facts.
                For each item include:
                - Date in **YYYY-MM-DD** format in IST timezone
                - Concise sentences summary from latest news
                - Sort news by date wise (latest first)
                - Source URL as link

                Use format:

                ### [Date]

                - [Summary](URL)
                """
            ),
            (
                "user",
                "Articles:\n{articles}"
            )
        ])
        
        articles_str = "\n\n".join([
            f"Content: {item.get('content', '')}\nURL: {item.get('url', '')}\nDate: {item.get('published_date', '')}"
            for item in news_items
        ])

        response = self.llm.invoke(prompt_template.format(articles=articles_str))

        state["summary"] = response.content

        return state

    def save_result(self, state: dict[str, Any]) -> dict[str, Any]:
        """
        Persist the final markdown summary to disk.
        """
        frequency = state.get("frequency", "weekly")
        topic_display = state.get("topic", "Artificial Intelligence")
        topic = self._slugify(str(topic_display))
        article_count = state.get("article_count", 5)
        summary = state.get("summary", "")

        self.output_dir.mkdir(parents=True, exist_ok=True)
        filename = self.output_dir / f"{topic}_{frequency}_{article_count}_summary.md"

        with filename.open("w", encoding="utf-8") as f:
            f.write(f"# {topic_display} AI News Summary\n\n")
            f.write(summary)

        state["filename"] = str(filename)
        return state


AiNewsNode = AINewsNode
