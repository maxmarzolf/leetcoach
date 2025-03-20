#!/usr/bin/env python

from langgraph.graph import StateGraph

from react_agent.configuration import Configuration
from react_agent.state import InputState, State
from react_agent.agents import gather_user_experience, graph_theory_tutor, graph_theory_assessment, tree_theory_tutor


builder = StateGraph(State, input=InputState, config_schema=Configuration)

builder.add_node(gather_user_experience)
builder.add_node(graph_theory_tutor)
# builder.add_node(tree_theory_tutor)
builder.add_node(graph_theory_assessment)

builder.add_edge("__start__", "gather_user_experience")
builder.add_edge("gather_user_experience", "graph_theory_tutor")
# builder.add_edge("gather_user_experience", "tree_theory_tutor")
builder.add_edge("graph_theory_tutor", "graph_theory_assessment")
builder.add_edge("graph_theory_assessment", "graph_theory_tutor")

graph = builder.compile(
    interrupt_before=["graph_theory_tutor", 'graph_theory_assessment'],
    interrupt_after=[],
)
graph.name = "ReAct Agent"

