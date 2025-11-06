from agno.workflow import StepInput, StepOutput
from bs4 import BeautifulSoup
import httpx


def pre_process_html(html: str) -> str:
    """
    Clean HTML by removing scripts, styles, and other non-text elements,
    while keeping structural and contextual tags.

    This ensures LLMs retain semantic context (headers, labels, etc.)
    for more accurate data extraction.
    """
    soup = BeautifulSoup(html, "html.parser")

    # Remove unnecessary tags
    for tag in soup(["script", "style", "noscript", "iframe", "svg", "meta", "link"]):
        tag.decompose()

    # Optionally remove inline styles and attributes
    for tag in soup.find_all(True):
        tag.attrs = {k: v for k, v in tag.attrs.items() if k in ["id", "class"]}

    # Focus on <body> content if available
    body = soup.body or soup
    return str(body)


async def main_step(step_input: StepInput) -> StepOutput:
    targets = step_input.previous_step_content
    results = []

    if targets is None:
        return StepOutput(content="No targets to process")

    async with httpx.AsyncClient(timeout=30) as client:
        for target in targets:
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                    "Accept": "*/*",
                    "Referer": target.url,
                }
                resp = await client.get(target.url, headers=headers)
                resp.raise_for_status()

                content_type = resp.headers.get("Content-Type", "")
                if "application/json" in content_type:
                    data = resp.json()
                    results.append({"bank": target.name, "type": "json", "data": data})
                    print(f"Main step: result for {target.name} -> {data}")
                else:
                    html = resp.text
                    filtered_html = pre_process_html(html)
                    results.append(
                        {"bank": target.name, "type": "html", "data": filtered_html}
                    )  # trim preview for debugging
                    print(
                        f"Main step: result for {target.name} -> {filtered_html[:500]}"
                    )
            except Exception as e:
                print(f"Error fetching {target.name}: {e}")

    return StepOutput(content=f"Processed {len(targets)} sites")
