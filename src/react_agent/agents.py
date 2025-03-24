from datetime import datetime, timezone
from typing import  List, Dict, Literal, cast

from langchain_core.runnables import RunnableConfig
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.types import interrupt

from react_agent.configuration import Configuration
from react_agent.utils import load_chat_model
from react_agent.state import State, HumanInput


def ask_human(state: State, config: RunnableConfig) -> Literal["graph_theory_tutor", "tree_theory_tutor"]:
    response = interrupt("Please provide feedback:")

    last_message = state.messages[-1]
    if 'graph theory' in last_message:
        return "graph_theory_tutor"
    else:
        return 'tree_theory_tutor'
    # else:
    #     return {"human_input": [response]}


async def gather_user_experience(state: State, config: RunnableConfig) -> Dict[str, List[AIMessage]]:
    configuration = Configuration.from_runnable_config(config)

    model = load_chat_model(configuration.model)

    system_message = configuration.gather_user_experience_prompt.format(
        system_time=datetime.now(tz=timezone.utc).isoformat()
    )

    response = cast(
        AIMessage,
        await model.ainvoke(
            [{"role": "system", "content": system_message}, *state.messages], config
        ),
    )

    return {"messages": [response]}



async def graph_theory_tutor(state: State, config: RunnableConfig) -> Dict[str, List[AIMessage]]:
    configuration = Configuration.from_runnable_config(config)

    model = load_chat_model(configuration.model)

    system_message = configuration.graph_theory.format(
        system_time=datetime.now(tz=timezone.utc).isoformat()
    )

    response = cast(
        AIMessage,
        await model.ainvoke(
            [{"role": "system", "content": system_message}, *state.messages], config
        ),
    )

    return {"messages": [response]}


async def graph_theory_assessment(state: State, config: RunnableConfig) -> Literal["__end__", "graph_theory_tutor"]:
    configuration = Configuration.from_runnable_config(config)
    model = load_chat_model(configuration.model)

    system_message = configuration.graph_theory_assessment.format(
        system_time=datetime.now(tz=timezone.utc).isoformat()
    )

    response = cast(
        AIMessage,
        await model.ainvoke(
            [{"role": "system", "content": system_message}, *state.messages], config
        ),
    )

    # Check if the agent has determined the user is sufficiently prepared.
    if "user is sufficiently prepared" in response.content.lower():
        return "__end__"
    else:
        return "graph_theory_tutor"


async def tree_theory_tutor(state: State, config: RunnableConfig) -> Dict[str, List[AIMessage]]:
    configuration = Configuration.from_runnable_config(config)

    model = load_chat_model(configuration.model)

    system_message = configuration.tree_theory_tutor.format(
        system_time=datetime.now(tz=timezone.utc).isoformat()
    )

    response = cast(
        AIMessage,
        await model.ainvoke(
            [{"role": "system", "content": system_message}, *state.messages], config
        ),
    )

    return {"messages": [response]}