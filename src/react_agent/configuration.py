"""Define the configurable parameters for the agent."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import Annotated, Optional

from langchain_core.runnables import RunnableConfig, ensure_config

from react_agent import prompts


@dataclass(kw_only=True)
class Configuration:
    """The configuration for the agent."""

    CLONE_GRAPH_133_CONCEPTUAL: str = field(
        default=prompts.CLONE_GRAPH_133_CONCEPTUAL,
        metadata={
            "description": "This agent prompt is used for training the clone graph problem."
            "This prompt sets the context and behavior for the agent."
        },
    )

    CLONE_GRAPH_133_CODE: str = field(
        default=prompts.CLONE_GRAPH_133_CODE,
        metadata={
            "description": "This agent prompt is used for training the clone graph code problem."
            "This prompt sets the context and behavior for the agent."
        },
    )

    CLONE_GRAPH_133_REAL_WORLD: str = field(
        default=prompts.CLONE_GRAPH_133_REAL_WORLD,
        metadata={
            "description": "This agent prompt is used for training the clone graph problem and highlights real world use cases."
            "This prompt sets the context and behavior for the agent."
        },
    )

    CLONE_GRAPH_133_ASSESSMENT: str = field(
        default=prompts.CLONE_GRAPH_133_ASSESSMENT,
        metadata={
            "description": "This agent prompt is used for assessing whether the user can move to a new node."
            "This prompt sets the context and behavior for the agent."
        },
    )

    model: Annotated[str, {"__template_metadata__": {"kind": "llm"}}] = field(
        default="openai/gpt-4o-mini-2024-07-18",
        metadata={
            "description": "The name of the language model to use for the agent's main interactions. "
            "Should be in the form: provider/model-name."
        },
    )

    max_search_results: int = field(
        default=10,
        metadata={
            "description": "The maximum number of search results to return for each search query."
        },
    )

    @classmethod
    def from_runnable_config(cls, config: Optional[RunnableConfig] = None) -> Configuration:
        """Create a Configuration instance from a RunnableConfig object."""
        config = ensure_config(config)
        configurable = config.get("configurable") or {}
        _fields = {f.name for f in fields(cls) if f.init}
        return cls(**{k: v for k, v in configurable.items() if k in _fields})
