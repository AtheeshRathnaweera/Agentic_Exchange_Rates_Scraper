from typing import List

from agno.workflow import StepInput, StepOutput

from app.models import ExchangeRate


async def save_to_db_step(step_input: StepInput) -> StepOutput:
    input: List[ExchangeRate] = step_input.previous_step_content

    # save the input to the postgresdb
