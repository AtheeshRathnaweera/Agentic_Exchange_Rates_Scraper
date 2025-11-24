import asyncio
import re
from typing import List
from agno.agent import RunOutput
from agno.workflow import StepInput, StepOutput
from bs4 import BeautifulSoup, Comment
import httpx

from agents import get_scraping_agent
from app.api.models.exchange_rate import ExchangeRate
from app.api.models.scrape_target import ScrapeTarget
from utils import get_logger

logger = get_logger(__name__)
scraping_agent = get_scraping_agent(debug_mode=True)


def pre_process_html(html: str) -> str:
    """
    Extract tables and nearby context that mention the keywords.

    Returns a list of HTML snippets for each relevant table + context.
    """
    logger.info("Starting HTML preprocessing...")
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

    logger.info("Preprocessing complete.")
    return minified_html


async def extract_rates_step(step_input: StepInput) -> StepOutput:
    """
    Extracts exchange rates from a list of scrape targets.
    """
    logger.info("Starting extraction step...")
    targets: List[ScrapeTarget] = step_input.previous_step_content
    results: List[ExchangeRate] = []

    if targets is None:
        logger.info("No targets to process. Exiting.")
        return StepOutput(content="No targets to process")

    logger.info("Processing %s targets.", len(targets))
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            for target in targets:
                logger.info("Fetching URL: %s (name: %s)", target.url, target.name)
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
                        logger.info(
                            "JSON content for %s: %s...", target.name, str(data)[:100]
                        )
                        agent_input = (
                            f"This is the raw JSON content from {target.name} Sri Lanka.\n"
                            f"System tag: {target.tag}\n"
                            f"{data}"
                        )
                    else:
                        html = resp.text
                        logger.info(
                            "HTML content for %s received. Preprocessing...",
                            target.name,
                        )
                        filtered_html = pre_process_html(html)
                        logger.info(
                            "Filtered HTML for %s: %s", target.name, filtered_html[:500]
                        )
                        agent_input = (
                            f"This is the raw HTML content from {target.name} Sri Lanka.\n"
                            f"System tag: {target.tag}\n"
                            f"{filtered_html}"
                        )

                    try:
                        logger.info("Running scraping agent for %s...", target.name)
                        response: RunOutput = scraping_agent.run(input=agent_input)
                        logger.info(
                            "Agent metrics for %s: %s", target.name, response.metrics
                        )
                        results.append(response.content)
                        # Only wait if there are more targets left to process
                        if target != targets[-1]:
                            logger.info(
                                "Waiting 01 minute before next call due to Groq API rate limit..."
                            )
                            await asyncio.sleep(60)
                    except Exception as e:
                        logger.error(
                            (
                                "❌ Error running agent for %s: %s",
                                target.name,
                                e,
                            ),
                            exc_info=True,
                        )
                except Exception as e:
                    logger.error(
                        ("Error fetching %s: %s", target.name, e),
                        exc_info=True,
                    )
        logger.info("Extraction step complete. %s results collected.", len(results))
        return StepOutput(content=results)
    except Exception as e:
        logger.error(
            ("Fatal error in AsyncClient: %s", e),
            exc_info=True,
        )
        return StepOutput(content=f"Fatal error: {e}", stop=True)
