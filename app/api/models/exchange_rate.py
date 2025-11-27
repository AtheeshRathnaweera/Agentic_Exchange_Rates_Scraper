from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class CurrencyRate(BaseModel):
    """
    Represents the detailed exchange rate information for a single currency, as published by a bank.
    """

    name: str = Field(..., description="Full name of the currency, e.g., US Dollar")
    code: str = Field(
        ..., description="Three-letter ISO 4217 currency code (e.g., 'USD')."
    )
    tt_buying: Optional[float] = Field(
        None, description="Telegraphic Transfer (TT) buying rate."
    )
    tt_selling: Optional[float] = Field(
        None, description="Telegraphic Transfer (TT) selling rate."
    )
    draft_buying: Optional[float] = Field(
        None, description="Draft or Overdraft (O/D) buying rate, if available."
    )
    draft_selling: Optional[float] = Field(
        None, description="Draft or Overdraft (O/D) selling rate, if available."
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
        None, description="Other or unspecified category buying rate, if available."
    )
    other_selling: Optional[float] = Field(
        None, description="Other or unspecified category selling rate, if available."
    )


class ExchangeRate(BaseModel):
    """
    Represents the complete set of exchange rates from a bank, including metadata.
    """

    bank_name: str = Field(
        ...,
        description="Official name of the bank providing the exchange rates (standardized format).",
    )
    country: str = Field("Sri Lanka", description="Country where the bank operates.")
    last_updated: Optional[datetime] = Field(
        ...,
        description="Timestamp (in ISO 8601 format) when the exchange rates were last updated or published.",
    )
    source_url: Optional[str] = Field(
        None, description="The original source URL where the rates were obtained"
    )
    rates: List[CurrencyRate] = Field(
        ...,
        description="List of structured currency exchange rate entries extracted from the source.",
    )
    notes: Optional[str] = (
        Field(
            None,
            description="Additional notes, remarks, or disclaimers extracted from the page (if available).",
        ),
    )
    tag: Optional[str] = Field(
        ...,
        description="System-provided identifier used for tracking or grouping extraction runs.",
    )
