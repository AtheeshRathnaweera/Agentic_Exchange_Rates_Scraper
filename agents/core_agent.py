from typing import List, Optional
from datetime import datetime

from agno.agent import Agent
from agno.models.groq import Groq
from pydantic import BaseModel, Field

from agents.fewshots import html_examples, json_examples


class CurrencyRate(BaseModel):
    name: str = Field(..., description="Full name of the currency, e.g., US Dollar")
    code: str = Field(..., description="ISO currency code, e.g., USD")
    tt_buying: Optional[float] = Field(
        None, description="Telegraphic Transfer buying rate"
    )
    tt_selling: Optional[float] = Field(
        None, description="Telegraphic Transfer selling rate"
    )
    draft_buying: Optional[float] = Field(
        None, description="Draft buying rate, if available"
    )
    draft_selling: Optional[float] = Field(
        None, description="Draft selling rate, if available"
    )
    cheques_buying: Optional[float] = Field(
        None, description="Cheques buying rate, if available"
    )
    cheques_selling: Optional[float] = Field(
        None, description="Cheques selling rate, if available"
    )
    currency_buying: Optional[float] = Field(
        None, description="Currency note buying rate, if available"
    )
    currency_selling: Optional[float] = Field(
        None, description="Currency note selling rate, if available"
    )
    other_buying: Optional[float] = Field(
        None, description="Other buying rate (e.g., O/D), if available"
    )
    other_selling: Optional[float] = Field(
        None, description="Other selling rate (e.g., O/D), if available"
    )


class ExchangeRateData(BaseModel):
    bank_name: str = Field(
        ..., description="Name of the bank providing the exchange rates"
    )
    country: str = Field("Sri Lanka", description="Country of the bank")
    last_updated: datetime = Field(
        ..., description="Timestamp when the rates were last updated"
    )
    source_url: Optional[str] = Field(
        None, description="URL where the rates were scraped from"
    )
    rates: List[CurrencyRate] = Field(
        ..., description="List of currency rates provided by the bank"
    )
    notes: Optional[str] = Field(
        None, description="Additional information or disclaimers from the bank"
    )


def get_core_agent(
    model_id: str = "llama-3.1-8b-instant",
    debug_mode: bool = False,
) -> Agent:
    return Agent(
        id="core-agent",
        name="Core Agent",
        model=Groq(id=model_id),
        additional_input=[html_examples, json_examples],
        description="Extracts exchange rate data from raw HTML or JSON from"
        "Sri Lankan bank websites.",
        instructions=[
            "Always output the data in strict JSON following the ExchangeRateData schema.",
            "Identify all currencies present and extract both TT and O/D rates if available.",
            "Include the source and timestamp for each extraction.",
        ],
        output_schema=ExchangeRateData,
        use_json_mode=True,
        debug_mode=debug_mode,
    )
