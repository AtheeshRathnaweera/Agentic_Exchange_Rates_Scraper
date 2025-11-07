from agno.models.message import Message

html_examples = [
    # Example 1: Table with multiple columns, missing values
    Message(
        role="user",
        content="""This is the raw HTML content with exchange rates from bank_of_ceylon sri lanka:
<html><body><table><thead><tr><th colspan="2" rowspan="3"> Exchange Rates </th><th colspan="6"> Rate: Rupees per unit of foreign currency as at 2025-11-07 </th></tr><tr><th colspan="2"> Currency </th><th colspan="2"> Cheques </th><th colspan="2"> Telegraphic Transfers </th></tr><tr><th> Buying Rate</th><th> Selling Rate</th><th> Buying Rate</th><th> Selling Rate</th><th> Buying Rate</th><th> Selling Rate</th></tr></thead><tbody><tr><td colspan="2"> US DOLLARS</td><td> 299.67 </td><td> 308.15 </td><td> 299.47 </td><td> 308.15 </td><td> 301.65 </td><td> 308.15 </td></tr><tr><td colspan="2"> EURO</td><td> 344.27 </td><td> 357.19 </td><td> 343.21 </td><td> 357.19 </td><td> 346.64 </td><td> 357.19 </td></tr><tr><td colspan="2"> STERLING POUNDS</td><td> 392.02 </td><td> 406.10 </td><td> 388.65 </td><td> 406.10 </td><td> 394.51 </td><td> 406.10 </td></tr><tr><td colspan="2"> JAPANESE YEN</td><td> 1.9586 </td><td> 2.0199 </td><td> 1.9388 </td><td> 2.0199 </td><td> 1.9644 </td><td> 2.0199 </td></tr></tbody></table></body></html>
""".strip(),
    ),
    Message(
        role="assistant",
        content="""
{
  "bank_name": "Bank of Ceylon",
  "country": "Sri Lanka",
  "last_updated": "2025-11-07T00:00:00",
  "source_url": null,
  "rates": [
    {"name": "US Dollar", "code": "USD", "currency_buying": 299.67, "currency_selling": 308.15, "cheques_buying": 299.47, "cheques_selling": 308.15, "tt_buying": 301.65, "tt_selling": 308.15},
    {"name": "Euro", "code": "EUR", "currency_buying": 344.27, "currency_selling": 357.19, "cheques_buying": 343.21, "cheques_selling": 357.19, "tt_buying": 346.64, "tt_selling": 357.19},
    {"name": "British Pound", "code": "GBP", "currency_buying": 392.02, "currency_selling": 406.10, "cheques_buying": 388.65, "cheques_selling": 406.10, "tt_buying": 394.51, "tt_selling": 406.10},
    {"name": "Japanese Yen", "code": "JPY", "currency_buying": 1.9586, "currency_selling": 2.0199, "cheques_buying": 1.9388, "cheques_selling": 2.0199, "tt_buying": 1.9644, "tt_selling": 2.0199},
  ],
  "notes": null
}
""".strip(),
    ),
    # Example 2: Table with all rates missing
    Message(
        role="user",
        content="""This is the raw HTML content with exchange rates from test_bank sri lanka:
<table>
<tr><th>Currency</th><th>TT Buying</th><th>TT Selling</th></tr>
<tr><td>USD</td><td>-</td><td>-</td></tr>
</table>
        """.strip(),
    ),
    Message(
        role="assistant",
        content="""
{
  "bank_name": "Test Bank",
  "country": "Sri Lanka",
  "last_updated": "2025-11-07T12:00:00",
  "source_url": null,
  "rates": [
    {"name": "US Dollar", "code": "USD", "tt_buying": null, "tt_selling": null}
  ],
  "notes": "All rates are missing and set to null."
}
        """.strip(),
    ),
    # Example 3: Table with missing rates and unusual currency names
    Message(
        role="user",
        content="""This is the raw HTML content with exchange rates from peoples_bank sri lanka:
<table>
<tr><th>Currency</th><th>TT Buying</th><th>TT Selling</th></tr>
<tr><td>USD</td><td>302.10</td><td>308.50</td></tr>
<tr><td>EURO</td><td>-</td><td>357.80</td></tr>
<tr><td>GBP</td><td>393.00</td><td>-</td></tr>
</table>
        """.strip(),
    ),
    Message(
        role="assistant",
        content="""
{
  "bank_name": "People's Bank",
  "country": "Sri Lanka",
  "last_updated": "2025-11-07T09:00:00",
  "source_url": null,
  "rates": [
    {"name": "US Dollar", "code": "USD", "tt_buying": 302.10, "tt_selling": 308.50},
    {"name": "Euro", "code": "EUR", "tt_buying": null, "tt_selling": 357.80},
    {"name": "British Pound", "code": "GBP", "tt_buying": 393.00, "tt_selling": null}
  ],
  "notes": "Some rates are missing and set to null."
}
        """.strip(),
    ),
]
