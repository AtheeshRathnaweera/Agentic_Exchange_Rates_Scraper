from typing import List
from agno.workflow import StepInput, StepOutput
from sqlalchemy.exc import SQLAlchemyError
from tenacity import retry, stop_after_attempt, wait_exponential
from app.models import ExchangeRate
from db.repositories import RawExchangeRateRepository
from db import get_db


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def save_bulk_with_retry(repo, objs):
    try:
        return repo.save_bulk(objs)
    except SQLAlchemyError as e:
        # Log error, optionally re-raise
        print(f"Database error: {e}")
        raise


async def save_to_db_step(step_input: StepInput) -> StepOutput:
    input_data: List[ExchangeRate] = step_input.previous_step_content

    # Convert ExchangeRate objects to dicts for bulk save
    rates_data = []
    for ex_rate in input_data:
        for rate in ex_rate.rates:
            rates_data.append(
                {
                    "bank_name": ex_rate.bank_name,
                    "country": ex_rate.country,
                    "last_updated": ex_rate.last_updated,
                    "source_url": ex_rate.source_url,
                    "currency_name": rate.name,
                    "currency_code": rate.code,
                    "tt_buying": rate.tt_buying,
                    "tt_selling": rate.tt_selling,
                    "draft_buying": rate.draft_buying,
                    "draft_selling": rate.draft_selling,
                    "cheques_buying": rate.cheques_buying,
                    "cheques_selling": rate.cheques_selling,
                    "currency_buying": rate.currency_buying,
                    "currency_selling": rate.currency_selling,
                    "other_buying": rate.other_buying,
                    "other_selling": rate.other_selling,
                    "notes": ex_rate.notes,
                    "tag": getattr(ex_rate, "tag", None),
                }
            )
    try:
        repo = RawExchangeRateRepository(db=get_db())
        saved_objs = save_bulk_with_retry(repo, rates_data)
        return StepOutput(content=f"{len(saved_objs)} items saved successfully")
    except Exception as e:
        return StepOutput(content=f"Error saving to DB: {str(e)}")
