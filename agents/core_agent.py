from typing import List

from agno.agent import Agent
from agno.models.groq import Groq
from pydantic import BaseModel, Field


class MovieScript(BaseModel):
    setting: str = Field(
        ..., description="Provide a nice setting for a blockbuster movie."
    )
    ending: str = Field(
        ...,
        description="Ending of the movie. If not available, provide a happy ending.",
    )
    genre: str = Field(
        ...,
        description="Genre of the movie. If not available, select action, thriller or romantic comedy.",
    )
    name: str = Field(..., description="Give a name to this movie")
    characters: List[str] = Field(..., description="Name of characters for this movie.")
    storyline: str = Field(
        ..., description="3 sentence storyline for the movie. Make it exciting!"
    )


def get_core_agent(
    model_id: str = "llama-3.1-8b-instant",
    debug_mode: bool = False,
) -> Agent:
    return Agent(
        id="core-agent",
        name="Core Agent",
        model=Groq(id=model_id),
        description="You help people write movie scripts.",
        output_schema=MovieScript,
        use_json_mode=True,
        debug_mode=debug_mode,
    )
