from datetime import datetime, timezone
from typing import List, Dict, Literal, cast
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

    return {"messages": [response], 'current_node': 'clone_graph_conceptual'}


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

    return {"messages": [response], 'current_node': 'clone_graph_code'}


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
        "next_node": state.next_node,
        "first_pass": state.first_pass
    }


async def clone_graph_assessment(state: State, config: RunnableConfig) -> State:
    """
    Updates the state. MUST set state.next_node for the assessment_router().
    """
    # State: {[], "__start__", "", True}
    messages = state.messages
    next_node = ""
    current_node = state.current_node
    first_pass = state.first_pass

    if state.first_pass == True:
        print("-----------------")
        print("STATE.FIRST_PASS == TRUE")
        print("-----------------")
        next_node = "ask_human"
        return {
            "messages": messages,
            "next_node": next_node,
            "current_node": current_node,
            "first_pass": False,
        }

    # check if answer was correct/good enough to move on
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

    # conditionals

    # if good response: next question node
    # if bad response: same question node

    """
    It seems like you're starting to implement the depth-first search (DFS) approach, but I would need a bit more detail to evaluate your performance effectively. Could you please share a more complete code snippet or your thought process behind your implementation? 

    Here are some guiding questions to help you elaborate:

    1. **Base Case Handling**: How are you planning to check if the node is None? 
    2. **Visited Dictionary**: Do you have a strategy to keep track of already cloned nodes to avoid infinite loops?
    3. **Cloning Logic**: How do you intend to clone the current node and its neighbors?

    Feel free to provide any part of your code or explanation, and I’ll assess your proficiency based on that!
    """

    return {
        "messages": messages + [response],
        "next_node": current_node,  # KeyError('')
        "current_node": current_node,
        "first_pass": first_pass
    }  # go back to previous question node

    """
    if len(state.reasoning_type) == 0:
        next_node = 'ask_human'
    # __start__ -> random clone -> assessment - pass -> human/questions -> assessment - parse
    if state.messages[-1].type == "ai":
        next_node = "ask_human"

    if 'proficient' in response.content and state.selector == 'clone_graph_conceptual':
        reasoning_type = random.choice(
            ['clone_graph_code', 'clone_graph_real_world'])
        next_node = reasoning_type

    if 'proficient' in response.content and state.selector == 'clone_graph_code':
        reasoning_type = random.choice(
            ['clone_graph_conceptual', 'clone_graph_real_world'])
        next_node = reasoning_type

    if 'proficient' in response.content and state.selector == 'clone_graph_real_world':
        reasoning_type = random.choice(
            ['clone_graph_conceptual', 'clone_graph_code'])
        next_node = reasoning_type"
    """
