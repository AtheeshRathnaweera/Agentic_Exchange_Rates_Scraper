from agno.models.message import Message

json_examples = [
    # Example 01: Single currency info
    Message(
        role="user",
        content="""This is the raw JSON content with exchange rates from sampath_bank sri lanka:
{
  "CurrCode": "AUD",
  "CurrName": "Australian Dollar",
  "TTBUY": "194.48",
  "TTSEL": "202.39",
  "ODBUY": "193.37",
  "ODSEL": "202.39",
  "RateWEF": "2025-11-06T08:19:19"
}
        """.strip(),
    ),
    Message(
        role="assistant",
        content="""
{
  "bank_name": "Sampath Bank",
  "country": "Sri Lanka",
  "last_updated": "2025-11-06T08:19:19",
  "source_url": null,
  "rates": [
    {"name": "Australian Dollar", "code": "AUD", "tt_buying": 194.48, "tt_selling": 202.39, "draft_buying": 193.37, "draft_selling": 202.39}
  ],
  "notes": null
}
        """.strip(),
    ),
    # Example 02: Multiple currencies
    Message(
        role="user",
        content="""This is the raw JSON content from commercial_bank sri lanka:
[
  {"CurrCode": "USD", "CurrName": "US Dollar", "TTBUY": "300.10", "TTSEL": "308.00"},
  {"CurrCode": "EUR", "CurrName": "Euro", "TTBUY": "345.00", "TTSEL": "355.00"}
]
    """.strip(),
    ),
    Message(
        role="assistant",
        content="""
{
  "bank_name": "Commercial Bank",
  "country": "Sri Lanka",
  "last_updated": "2025-11-07T09:00:00",
  "source_url": null,
  "rates": [
    {"name": "US Dollar", "code": "USD", "tt_buying": 300.10, "tt_selling": 308.00},
    {"name": "Euro", "code": "EUR", "tt_buying": 345.00, "tt_selling": 355.00}
  ],
  "notes": null
}
    """.strip(),
    ),
]
