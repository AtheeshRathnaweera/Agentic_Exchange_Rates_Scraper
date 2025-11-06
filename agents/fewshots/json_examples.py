from agno.models.message import Message

json_examples = [
    Message(
        role="user",
        content="""
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
  "source": "JSON Bank API",
  "timestamp": "2025-11-06T08:19:19",
  "rates": [
    {"currency_code": "AUD", "currency_name": "Australian Dollar", "buying_tt": 194.48, "selling_tt": 202.39, "buying_od": 193.37, "selling_od": 202.39}
  ]
}
        """.strip(),
    ),
]
