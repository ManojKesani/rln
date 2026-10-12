"""Builds the LangChain agent for one request.

create_agent() returns a compiled LangGraph graph. With no tools it is simply
"call the model once". Once tools exist (S-009) the same graph becomes a loop:
model -> tool -> model -> ... until the model answers without a tool call.

The checkpointer is what gives the agent memory: before each run LangGraph loads
the saved state for config["configurable"]["thread_id"], and after the run it
saves the new state. The agent object itself holds nothing, so building one per
request is cheap and safe.
"""
from langchain.agents import create_agent


def build_agent(chat_model, checkpointer, system_prompt: str | None = None, tools: list | None = None):
    return create_agent(
        model=chat_model,
        tools=tools or [],            # [] = tool-less for now
        system_prompt=system_prompt,  # None = no system message (prompts arrive in S-010/S-011)
        checkpointer=checkpointer,    # persists state per thread_id
    )
