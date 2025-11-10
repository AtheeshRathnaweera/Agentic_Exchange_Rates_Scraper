from typing import List

from sqlalchemy.exc import SQLAlchemyError
from tenacity import retry, stop_after_attempt, wait_exponential

from agno.workflow import StepInput, StepOutput
from app.models import ExchangeRate
from db.models import RawExchangeRate
from db.repositories import RawExchangeRateRepository
from db import get_db


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def save_bulk_with_retry(repo, objs):
    """
    Attempts to save a list of objects to the database using the provided repository.
    Retries up to 3 times with exponential backoff on failure.
    """
    print(
        f"[save_bulk_with_retry] Attempting to save {len(objs)} objects using {type(repo).__name__}..."
    )
    try:
        result = repo.save_bulk(objs)
        print(f"[save_bulk_with_retry] Successfully saved {len(result)} objects.")
        return result
    except SQLAlchemyError as e:
        print(f"[save_bulk_with_retry] Database error: {e}")
        raise
    except Exception as e:
        print(f"[save_bulk_with_retry] Unexpected error: {e}")
        raise


async def save_to_db_step(step_input: StepInput) -> StepOutput:
    """
    Async workflow step to save extracted exchange rates to the database.
    """
    print("[save_to_db_step] Starting save to DB step...")
    input_data: List[ExchangeRate] = step_input.previous_step_content
    meatadata = step_input.workflow_session.metadata or {}
    correlation_id = meatadata.get("correlation_id")

    print(f"[save_to_db_step] correlation_id: {correlation_id}")

    # Convert ExchangeRate objects to dicts for bulk save
    rates_data: List[RawExchangeRate] = []
    for ex_rate in input_data:
        for rate in ex_rate.rates:
            rates_data.append(
                RawExchangeRate(
                    bank_name=ex_rate.bank_name,
                    country=ex_rate.country,
                    last_updated=ex_rate.last_updated,
                    source_url=ex_rate.source_url,
                    currency_name=rate.name,
                    currency_code=rate.code,
                    tt_buying=rate.tt_buying,
                    tt_selling=rate.tt_selling,
                    draft_buying=rate.draft_buying,
                    draft_selling=rate.draft_selling,
                    cheques_buying=rate.cheques_buying,
                    cheques_selling=rate.cheques_selling,
                    currency_buying=rate.currency_buying,
                    currency_selling=rate.currency_selling,
                    other_buying=rate.other_buying,
                    other_selling=rate.other_selling,
                    notes=ex_rate.notes,
                    tag=getattr(ex_rate, "tag", None),
                    correlation_id=correlation_id,
                ),
            )
    print(f"[save_to_db_step] Prepared {len(rates_data)} records for saving.")
    try:
        repo = RawExchangeRateRepository(db=next(get_db()))
        print("[save_to_db_step] Repository initialized. Saving records...")
        saved_objs = save_bulk_with_retry(repo, rates_data)
        print(
            f"[save_to_db_step] Save operation completed. {len(saved_objs)} items saved."
        )
        return StepOutput(content=f"{len(saved_objs)} items saved successfully")
    except Exception as e:
        print(f"[save_to_db_step] Error saving to DB: {str(e)}")
        return StepOutput(content=f"Error saving to DB: {str(e)}")
