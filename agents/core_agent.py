from typing import List, Optional
from datetime import datetime

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.models.groq import Groq
from pydantic import BaseModel, Field

from agents.fewshots import html_examples, json_examples

from db.session import db_url


class CurrencyRate(BaseModel):
    """
    Represents the exchange rate details for a single currency from a bank.
    """

    name: str = Field(..., description="Full name of the currency, e.g., US Dollar")
    code: str = Field(..., description="ISO currency code, e.g., USD")
    tt_buying: Optional[float] = Field(
        None, description="Telegraphic Transfer buying rate"
    )
    tt_selling: Optional[float] = Field(
        None, description="Telegraphic Transfer selling rate"
    )
    draft_buying: Optional[float] = Field(
        None, description="Draft buying rate (e.g., O/D), if available"
    )
    draft_selling: Optional[float] = Field(
        None, description="Draft selling rate (e.g., O/D), if available"
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
        None, description="Other buying rate, if available"
    )
    other_selling: Optional[float] = Field(
        None, description="Other selling rate, if available"
    )


class ExchangeRateData(BaseModel):
    """
    Represents the complete set of exchange rates from a bank, including metadata.
    """

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
    """
    Creates and returns the core agent for extracting exchange rate data from Sri Lankan
    bank websites.

    Args:
        model_id (str): The model identifier to use for extraction
        (default: 'llama-3.1-8b-instant').
        debug_mode (bool): If True, enables debug mode for the agent (default: False).

    Returns:
        Agent: Configured agent instance for extracting and structuring exchange rate data.
    """
    return Agent(
        id="core-agent",
        name="Core Agent",
        model=Groq(id=model_id),
        additional_input=[html_examples, json_examples],
        description="Extracts structured exchange rate data from Sri Lankan bank HTML or "
        "JSON content.",
        instructions=[
            "Detect whether the input is HTML or JSON.",
            "Output only valid JSON following the ExchangeRateData schema.",
            "Identify all currencies and rate categories: TT, O/D, Cheques, Currency Notes, etc.",
            "Map categories to fields as follows: "
            "Currency → currency_buying/currency_selling; "
            "Cheques → cheques_buying/cheques_selling; "
            "Overdraft, Drafts, O/D, ODBUY, ODSELL, OD_SELL → draft_buying/draft_selling; "
            "Telegraphic Transfer → tt_buying/tt_selling; "
            "Others → other_buying/other_selling.",
            "When reading HTML tables, always match each numeric column under its correct header. "
            "For example, ensure 'Currency → Buying Rate' maps to currency_buying, "
            "'Currency → Selling Rate' maps to currency_selling, "
            "'Cheques → Buying Rate' maps to currency_buying, "
            "'Cheques → Selling Rate' maps to cheques_selling, etc.",
            "Do not assume column order — use the table headers and hierarchy (even with colspan/rowspan) to map rates precisely.",
            "Include source URL and timestamp in each result.",
            "Standardize currencies using ISO codes and bank names "
            "(e.g., sampath_bank → Sampath Bank, hsbc_sri_lanka → HSBC Sri Lanka).",
        ],
        output_schema=ExchangeRateData,
        use_json_mode=True,
        debug_mode=debug_mode,
    )
