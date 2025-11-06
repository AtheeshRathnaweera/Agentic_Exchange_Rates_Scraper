from agno.models.message import Message

html_examples = [
    Message(
        role="user",
        content="""
<table>
<tr><td>USD</td><td>301.40</td><td>307.90</td></tr>
<tr><td>EUR</td><td>344.93</td><td>356.05</td></tr>
</table>
        """.strip(),
    ),
    Message(
        role="assistant",
        content="""
{
  "source": "Sample Bank",
  "timestamp": "2025-11-06T08:19:19",
  "rates": [
    {"currency_code": "USD", "currency_name": "US Dollar", "buying_tt": 301.40, "selling_tt": 307.90},
    {"currency_code": "EUR", "currency_name": "Euro", "buying_tt": 344.93, "selling_tt": 356.05}
  ]
}
        """.strip(),
    ),
    # Example 2: Table with headers and O/D rates
    Message(
        role="user",
        content="""
<table>
<tr><td>USD</td><td>301.75</td><td>308.25</td><td>300.95</td><td>308.25</td></tr>
<tr><td>GBP</td><td>392.36</td><td>404.26</td><td>391.13</td><td>403.74</td></tr>
</table>
        """.strip(),
    ),
    Message(
        role="assistant",
        content="""
{
  "source": "Bank XYZ",
  "timestamp": "2025-11-06T11:00:04",
  "rates": [
    {"currency_code": "USD", "currency_name": "US Dollar", "buying_tt": 301.75, "selling_tt": 308.25, "buying_od": 300.95, "selling_od": 308.25},
    {"currency_code": "GBP", "currency_name": "British Pound", "buying_tt": 392.36, "selling_tt": 404.26, "buying_od": 391.13, "selling_od": 403.74}
  ]
}
        """.strip(),
    ),
    # Example 3: Complex table with multiple columns
    Message(
        role="user",
        content="""
<table>
<tr><th>Currency</th><th>Buying Rate</th><th>Selling Rate</th><th>Drafts Buying</th><th>Drafts Selling</th></tr>
<tr><td>EUR</td><td>344.90</td><td>356.90</td><td>341.40</td><td>355.72</td></tr>
<tr><td>JPY</td><td>1.9406</td><td>2.0206</td><td>1.9314</td><td>2.0209</td></tr>
</table>
        """.strip(),
    ),
    Message(
        role="assistant",
        content="""
{
  "source": "Another Bank",
  "timestamp": "2025-11-06T11:30:00",
  "rates": [
    {"currency_code": "EUR", "currency_name": "Euro", "buying_tt": 344.90, "selling_tt": 356.90, "buying_od": 341.40, "selling_od": 355.72},
    {"currency_code": "JPY", "currency_name": "Japanese Yen", "buying_tt": 1.9406, "selling_tt": 2.0206, "buying_od": 1.9314, "selling_od": 2.0209}
  ]
}
        """.strip(),
    ),
]
