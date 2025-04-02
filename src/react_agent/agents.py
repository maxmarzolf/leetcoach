from datetime import datetime, timezone
from typing import  List, Dict, Literal, cast
import random

from langchain_core.runnables import RunnableConfig
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.types import interrupt, Command

from react_agent.configuration import Configuration
from react_agent.utils import load_chat_model
from react_agent.state import State


def ask_human(state: State, config: RunnableConfig) -> Literal["graph_theory_tutor", "tree_theory_tutor"]:
    response = interrupt("Please provide input:")
    return {"human_input": [response]}


def selector(state: State) -> Literal["clone_graph_conceptual", "clone_graph_code", "clone_graph_real_world"]:
    options = ["clone_graph_conceptual", "clone_graph_code", "clone_graph_real_world"]

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


async def clone_graph_assessment(state: State, config: RunnableConfig) -> Command[Literal['ask_human', 'clone_graph_conceptual', 'clone_graph_code', 'clone_graph_real_world']]:
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


    print("BOBS HERE1")
    print(response)
    print("BOBS HERE1")

    print("BOBS HERE2")
    print(state.selector)
    print("BOBS HERE2")

    print("BOBS HERE3")
    print(state)
    print("BOBS HERE3")

    print('1')



    if len(state.reasoning_type) == 0:
        next_node = 'ask_human'
        print('2')


    if 'proficient' in response.content and state.selector == 'clone_graph_conceptual':
        reasoning_type = random.choice(['clone_graph_code', 'clone_graph_real_world'])
        next_node = reasoning_type
        print('3')

    
    if 'proficient' in response.content and state.selector == 'clone_graph_code':
        reasoning_type = random.choice(['clone_graph_conceptual', 'clone_graph_real_world'])
        next_node = reasoning_type
        print('4')

        
    if 'proficient' in response.content and state.selector == 'clone_graph_real_world':
        reasoning_type = random.choice(['clone_graph_conceptual', 'clone_graph_code'])
        next_node = reasoning_type
        print('5')

    print('6')
    # return Command(update={"reasoning_type": next_node}, goto=next_node) 
    return {"reasoning_type": next_node}

