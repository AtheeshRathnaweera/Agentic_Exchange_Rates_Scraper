import re
from typing import List
from agno.agent import RunOutput
from agno.workflow import StepInput, StepOutput
from bs4 import BeautifulSoup, Comment
import httpx
from agents import get_core_agent
from app.models import ExchangeRate, ScrapeTarget

core_agent = get_core_agent(debug_mode=True)


def pre_process_html(html: str) -> str:
    """
    Extract tables and nearby context that mention the keywords.

    Returns a list of HTML snippets for each relevant table + context.
    """
    if keywords is None:
        # Only match strong multi-word terms to avoid false positives
        keywords = [
            "exchange rate",
            "exchange rates",
            "currency exchange",
            "telegraphic transfer",
            "telegraphic transfers",
            "tt buying",
            "tt selling",
            "buying rate",
            "selling rate",
        ]

    soup = BeautifulSoup(html, "html5lib")

    # Remove all HTML comments
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()

    # Remove all attributes
    for tag in soup.find_all(True):
        # tag.attrs = {}
        if "class" in tag.attrs:
            del tag.attrs["class"]
        if "style" in tag.attrs:
            del tag.attrs["style"]
        if "width" in tag.attrs:
            del tag.attrs["width"]

    # Unwrap tags that add no meaning (keep text inside them)
    for unwrap_tag in [
        "p",
        "span",
    ]:
        for tag in soup.find_all(unwrap_tag):
            tag.unwrap()

    relevant_snippets = set()
    # Search all tags for keyword matches
    for tag in soup.find_all(True):
        text = tag.get_text(" ", strip=True).lower()
        if any(word in text for word in keywords):
            # Keep the tag itself and nearest table if exists
            parent_section = tag.find_parent(["div", "section", "body"]) or tag
            # Include all tables inside this parent
            for table in parent_section.find_all("table"):
                # --- New check: keep table only if it contains the keywords ---
                table_text = table.get_text(" ", strip=True).lower()
                if not any(word in table_text for word in keywords):
                    continue

                snippet = ""
                # Include nearest previous header if any
                for sibling in table.find_previous_siblings():
                    if sibling.name and sibling.name.startswith("h"):
                        snippet += f"<h3>{sibling.get_text(strip=True)}</h3>"
                        break
                snippet += str(table)
                relevant_snippets.add(snippet)

    # Combine all snippets into one HTML string
    combined_html = "\n".join(relevant_snippets)

    # Remove empty tags
    clean_soup = BeautifulSoup(combined_html, "html5lib")
    for tag in clean_soup.find_all():
        if not tag.get_text(strip=True):
            tag.decompose()

    # Minify whitespace
    minified_html = re.sub(r">\s+<", "><", str(clean_soup))
    minified_html = re.sub(r"\s+", " ", minified_html).strip()

    return minified_html


async def extract_rates_step(step_input: StepInput) -> StepOutput:
    targets: List[ScrapeTarget] = step_input.previous_step_content
    results: List[ExchangeRate] = []

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
                agent_input = ""

                if "application/json" in content_type:
                    data = resp.json()
                    print(f"Main step: result for {target.name} -> {data}")
                    agent_input = (
                        f"This is the raw JSON content from {target.name} Sri Lanka.\n"
                        f"System tag: {target.tag}\n"
                        f"{data}"
                    )
                else:
                    html = resp.text
                    filtered_html = pre_process_html(html)
                    print(
                        f"Main step: result for {target.name} -> {filtered_html[:500]}"
                    )
                    agent_input = (
                        f"This is the raw HTML content from {target.name} Sri Lanka.\n"
                        f"System tag: {target.tag}\n"
                        f"{filtered_html}"
                    )

                try:
                    response: RunOutput = core_agent.run(input=agent_input)
                    print("Metrics: ", response.metrics)
                    results.append(response.content)
                except Exception as e:
                    print(f"❌ Error: {e}")
                finally:
                    print("Main: run scraper completed")

                # call the agent to extract exchange rates
            except Exception as e:
                print(f"Error fetching {target.name}: {e}")

    return StepOutput(content=results)
