from dataclasses import dataclass


@dataclass
class ScrapeTarget:
    name: str
    url: str
    tag: str
