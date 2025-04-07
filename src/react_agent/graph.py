#!/usr/bin/env python

from langgraph.graph import StateGraph

from react_agent.config import Configuration
from react_agent.state import InputState, State
from react_agent.agents import ask_human, selector, assessment_router, clone_graph_conceptual, clone_graph_code, clone_graph_real_world, clone_graph_assessment
import asyncio

from frontend.initial import user_input

builder = StateGraph(State, input=InputState, config_schema=Configuration)

builder.add_node(ask_human)
builder.add_node(clone_graph_conceptual)
builder.add_node(clone_graph_code)
builder.add_node(clone_graph_real_world)
# builder.add_node(clone_graph_assessment)


builder.add_conditional_edges("__start__", selector)

builder.add_edge("clone_graph_conceptual", 'ask_human')
builder.add_edge("clone_graph_code", 'ask_human')
builder.add_edge("clone_graph_real_world", "ask_human")

builder.add_edge("ask_human", "clone_graph_assessment")


builder.add_node(clone_graph_assessment)
builder.add_conditional_edges("clone_graph_assessment", assessment_router, path_map=[
                                'clone_graph_conceptual', 'clone_graph_code', 'clone_graph_real_world'])


builder.add_edge("ask_human", "__end__")

graph = builder.compile(
    interrupt_before=[],
    interrupt_after=[],
)
graph.name = "ReAct Agent"





async def stream_graph_updates(user_input: str):
    async for event in graph.astream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)



async def main():
    while True:
        try:
            if user_input in ["quit", "exit", "q"]:
                print("Goodbye!")
                break

            await stream_graph_updates(user_input)
        except Exception as error:
            print(error)
            break

if __name__ == "__main__":
    asyncio.run(main())

