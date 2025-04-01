from datetime import datetime, timezone
from typing import  List, Dict, Literal, cast
import random

from langchain_core.runnables import RunnableConfig
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.types import interrupt

from react_agent.configuration import Configuration
from react_agent.utils import load_chat_model
from react_agent.state import State, HumanInput


def ask_human(state: State, config: RunnableConfig) -> Literal["graph_theory_tutor", "tree_theory_tutor"]:
    response = interrupt("Please provide input:")
    return {"human_input": [response]}


def selector(state: State) -> Literal["clone_graph_conceptual", "clone_graph_code", "clone_graph_real_world"]:
    options = ["clone_graph_conceptual", "clone_graph_code", "clone_graph_real_world"]
    print('BOBS HERE')
    print(state.selector)
    print('BOBS HERE')

    if len(state.selector) > 0:
        return state.selector
    else:
        return random.choice(options)


async def clone_graph_conceptual(state: State, config: RunnableConfig) -> Dict[str, List[AIMessage]]:
    configuration = Configuration.from_runnable_config(config)

    model = load_chat_model(configuration.model)

    system_message = configuration.CLONE_GRAPH_133_CONCEPTUAL.format(
        system_time=datetime.now(tz=timezone.utc).isoformat()
    )

    response = cast(
        AIMessage,
        await model.ainvoke(
            [{"role": "system", "content": system_message}, *state.messages], config
        ),
    )

    return {"messages": [response], 'selector': 'clone_graph_conceptual'}


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

    return {"messages": [response], 'selector': 'clone_graph_code'}


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

    return {"messages": [response], 'selector': 'clone_graph_code'}