from agno.agent import Agent
from agno.models.groq import Groq

from agents.fewshots import html_examples, json_examples
from app.api.models.exchange_rate import ExchangeRate


def get_scraping_agent(
    model_id: str = "openai/gpt-oss-120b",
    debug_mode: bool = False,
) -> Agent:
    """
    Creates and returns the scraping agent for extracting exchange rate data from Sri Lankan
    bank websites.

    Args:
        model_id (str): The model identifier to use for extraction
        (default: 'openai/gpt-oss-120b').
        debug_mode (bool): If True, enables debug mode for the agent (default: False).

    Returns:
        Agent: Configured agent instance for extracting and structuring exchange rate data.
    """
    return Agent(
        id="scraping-agent",
        name="Scraping Agent",
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
            "If a 'tag' value is provided in the input message, include it exactly as-is in the 'tag' field of the output JSON.",
            "Standardize currencies using ISO codes and bank names "
            "(e.g., sampath_bank → Sampath Bank, hsbc_sri_lanka → HSBC Sri Lanka).",
            "Map HNB API: buyingRate → tt_buying, sellingRate → tt_selling.",
        ],
        output_schema=ExchangeRate,
        # use_json_mode=True,
        debug_mode=debug_mode,
        # Save metrics to the DB -> https://github.com/agno-agi/agno/blob/main/cookbook/db/postgres/postgres_for_agent.py
    )
