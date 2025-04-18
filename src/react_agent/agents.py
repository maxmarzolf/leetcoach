from datetime import datetime, timezone
from typing import List, Dict, Literal, cast
import random

from langchain_core.runnables import RunnableConfig
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.types import interrupt

from react_agent.config import Configuration
from react_agent.utils import load_chat_model
from react_agent.state import State

import dataclasses


async def ask_human(state: State) -> HumanMessage:
    response = interrupt("Please provide input")
    return HumanMessage(content=response)


def selector(state: State) -> Literal["clone_graph_conceptual", "clone_graph_code", "clone_graph_real_world"]:
    options = ["clone_graph_conceptual",
               "clone_graph_code", "clone_graph_real_world"]

    if len(state.current_node) > 0:
        return state.current_node
    else:
        return random.choice(options)


def assessment_router(state: State) -> Literal["clone_graph_conceptual", "clone_graph_code", "clone_graph_real_world", "ask_human"]:
    return state.next_node


async def clone_graph_conceptual(state: State, config: RunnableConfig) -> Dict[str, List[AIMessage]]:
    configuration = Configuration.from_runnable_config(config)
    model = load_chat_model(config.model)

    system_message = configuration.CLONE_GRAPH_133_CONCEPTUAL.format(
        system_time=datetime.now(tz=timezone.utc).isoformat()
    )

    response = cast(
        AIMessage,
        await model.ainvoke(
            [{"role": "system", "content": system_message}, *state.messages], config
        ),
    )

    return {
        "messages": state.messages + [response],
        'current_node': 'clone_graph_conceptual',
        "next_node": state.next_node
    }


async def clone_graph_code(state: State, config: RunnableConfig) -> Dict[str, List[AIMessage]]:
    configuration = Configuration.from_runnable_config(config)
    model = load_chat_model(configuration.model)

    system_message = configuration.CLONE_GRAPH_133_CODE.format(
        system_time=datetime.now(tz=timezone.utc).isoformat()
    )

    response = cast(
        AIMessage,
        await model.ainvoke(
            [{"role": "system", "content": system_message}, *state.messages], config
        ),
    )

    return {
        "messages": state.messages + [response],
        'current_node': 'clone_graph_code',
        "next_node": state.next_node
    }


async def clone_graph_real_world(state: State, config: RunnableConfig) -> Dict[str, List[AIMessage]]:
    configuration = Configuration.from_runnable_config(config)
    model = load_chat_model(configuration.model)

    system_message = configuration.CLONE_GRAPH_133_REAL_WORLD.format(
        system_time=datetime.now(tz=timezone.utc).isoformat()
    )

    response = cast(
        AIMessage,
        await model.ainvoke(
            [{"role": "system", "content": system_message}, *state.messages], config
        ),
    )

    return {
        "messages": state.messages + [response],
        'current_node': 'clone_graph_real_world',
        "next_node": state.next_node
    }


async def clone_graph_assessment(state: State, config: RunnableConfig) -> State:
    """
    Updates the state. MUST set state.next_node for the assessment_router().
    """
    next_node = ""

    configuration = Configuration.from_runnable_config(config)
    model = load_chat_model(configuration.model)
    system_message = configuration.CLONE_GRAPH_133_ASSESSMENT.format(
        system_time=datetime.now(tz=timezone.utc).isoformat()
    )

    response = cast(
        AIMessage,
        await model.ainvoke(
            [{"role": "system", "content": system_message}, *state.messages], config
        ),
    )

    if "evaluation: user is proficient" in response.content:
        nodes = ['clone_graph_code', 'clone_graph_real_world',
                 'clone_graph_conceptual']
        next_node = random.choice(
            [n for n in nodes if n != state.current_node]
        )

        return dataclasses.replace(state, messages=state.messages + [response], next_node=next_node)
    else:
        return dataclasses.replace(state, messages=state.messages + [response], next_node=state.current_node)
