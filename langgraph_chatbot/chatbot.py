from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_groq import ChatGroq
from langgraph_chatbot.config import Config
from langgraph_chatbot.utils import logger
from langgraph_chatbot.tools import tools

class State(TypedDict):
    messages: Annotated[list, add_messages]

def build_chatbot():
    try:
        llm = ChatGroq(
            api_key=Config.GROQ_API_KEY,
            model="deepseek-r1-distill-llama-70b",
            temperature=0,
            max_tokens=1000,
            reasoning_format="parsed",
            timeout=None,
            max_retries=2,
        )

        graph_builder = StateGraph(State)
        llm_with_tools = llm.bind_tools(tools=tools)

        def chatbot(state: State):
            logger.debug("Invoking model with state: %s", state)
            return {"messages": llm_with_tools.invoke(state["messages"])}

        graph_builder.add_node("chatbot", chatbot)
        tool_node = ToolNode(tools=tools)
        graph_builder.add_node("tools", tool_node)

        graph_builder.add_edge(START, "chatbot")
        graph_builder.add_conditional_edges("chatbot", tools_condition)
        graph_builder.add_edge("tools", "chatbot")
        graph_builder.add_edge("chatbot", END)

        return graph_builder.compile()

    except Exception as e:
        logger.error("Failed to build chatbot: %s", str(e))
        raise
