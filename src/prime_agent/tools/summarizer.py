"""
summarizer.py – Option C: Full multi-page pipeline

Features:
- Crawl a root URL (e.g. a tutorial index page)
- Follow internal links (same domain) up to max_pages
- Extract main textual content
- Merge everything into one big context
- Generate a Master Study Guide using LLMClient

Requires:
    pip install requests beautifulsoup4
"""

from __future__ import annotations

from typing import List, Set
import logging
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from prime_agent.llm.client import LLMClient
from prime_agent.config import DEFAULT_MODEL


# ---------------------------------------------------------------------------
# 1. HTML TEXT EXTRACTION
# ---------------------------------------------------------------------------

def _extract_main_text(html: str) -> str:
    """
    Extracts the main readable text from HTML:
    - Drops scripts, styles, nav, footer, etc.
    - Keeps headings, paragraphs, list items, code, and preformatted text.
    """
    soup = BeautifulSoup(html, "html.parser")

    # Remove clutter
    for tag in soup(
        [
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "noscript",
            "svg",
            "img",
            "form",
            "button",
            "input",
            "aside",
        ]
    ):
        tag.decompose()

    # Prefer article/main/content-like containers if present
    candidates = []
    for selector in ["article", "main", "div#content", "div.post", "div.entry-content", "section"]:
        el = soup.select_one(selector)
        if el:
            candidates.append(el)

    node = candidates[0] if candidates else (soup.body or soup)

    parts: List[str] = []
    for tag in node.find_all(["h1", "h2", "h3", "h4", "p", "li", "pre", "code", "table"]):
        text = tag.get_text(" ", strip=True)
        if text:
            parts.append(text)

    return "\n".join(parts)


# ---------------------------------------------------------------------------
# 2. SIMPLE SAME-DOMAIN CRAWLER
# ---------------------------------------------------------------------------

def crawl_and_merge(
    root_url: str,
    max_pages: int = 15,
    same_domain: bool = True,
    timeout: int = 10,
) -> str:
    """
    Crawls starting from root_url, visits up to max_pages HTML pages on the
    same domain, extracts main text from each page and returns one big string.
    """

    parsed_root = urlparse(root_url)
    domain = parsed_root.netloc

    to_visit: List[str] = [root_url]
    visited: Set[str] = set()
    collected_texts: List[str] = []

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)

        if url in visited:
            continue

        try:
            resp = requests.get(url, timeout=timeout)
        except requests.RequestException:
            logging.warning("Failed to fetch %s", url)
            continue

        content_type = resp.headers.get("Content-Type", "")
        if resp.status_code != 200 or "text/html" not in content_type:
            continue

        visited.add(url)

        html = resp.text
        text = _extract_main_text(html)
        if text.strip():
            collected_texts.append(text)

        # Discover more links
        soup = BeautifulSoup(html, "html.parser")
        for a in soup.find_all("a", href=True):
            link = urljoin(url, a["href"])
            parsed = urlparse(link)

            # Skip non-http(s), fragments, mailto, etc.
            if parsed.scheme not in ("http", "https"):
                continue
            if parsed.fragment:
                continue
            if same_domain and parsed.netloc != domain:
                continue
            if link in visited or link in to_visit:
                continue

            to_visit.append(link)

    return "\n\n".join(collected_texts)


# ---------------------------------------------------------------------------
# 3. LLM STUDY-GUIDE GENERATION
# ---------------------------------------------------------------------------

def generate_learning_content(context: str, topic: str, mode: str = "study_guide") -> str:
    """
    Core function that turns a big text context into a Master Study Guide
    using the configured LLM model.
    """
    client = LLMClient(model_name=DEFAULT_MODEL)
    # Keep context within safe limit for tokens
    safe_context = context[:40000]

    if mode != "study_guide":
        return f"Invalid mode selected: {mode}"

    # System prompt: teacher persona
    system_prompt = (
        "You are an expert university-level educator. "
        "You transform messy, multi-source raw text into a single, clear, deeply "
        "structured MASTER STUDY GUIDE that is accurate, complete, and easy to revise from. "
        "You avoid generic filler and focus on depth, clarity, and structure."
    )

    # Option C style prompt
    prompt = f"""
You will receive raw extracted content from one or multiple sources
(web pages, PDFs, articles, books, tutorials, reports).

Your job is to create the highest-quality, deeply structured, accurate,
and complete **Master Study Guide** for the topic:

🟥 Topic: {topic}

====================================================
RULES (OPTION C – MULTI-SOURCE MODE)
====================================================
1. You MUST reconstruct missing structure logically.
2. If the source text is shallow or fragmented, you MUST enrich it with
   clear explanations and organization, but stay within the topic.
3. Merge all ideas from the source into one coherent guide.
4. No vague or generic statements.
5. Do NOT introduce facts clearly unrelated to the topic.
6. Always keep the output well-formatted and complete.

====================================================
OUTPUT FORMAT
====================================================

# 📘 {topic}: Complete Master Study Guide

## 1. Core Concepts & Definitions
- Define all major concepts clearly.
- Expand short definitions into full explanations.
- Explain why each concept matters.

## 2. Full Breakdown of All Subtopics
For every relevant concept:
- Use a clear heading.
- Provide a deep explanation.
- Add examples (conceptual, real-world, code, etc. depending on the subject).

## 3. Processes, Workflows, Pipelines, or Algorithms
If the topic involves any sequence of steps:
- Write them as a numbered list.
- Explain each step.
- Mention when/why the process is used.

## 4. Detailed Tables (MANDATORY IF APPLICABLE)
Generate clean, well-formatted tables ONLY IF the topic naturally contains
classifications, categories, types, or comparisons.

STRICT TABLE RULES:
- NEVER merge multiple unrelated tables into one.
- NEVER write multiple tables on a single line.
- NEVER include raw text from the source directly inside the table header row.
- NEVER duplicate columns.
- If the source contains fragmented or repetitive headings, IGNORE them.
- Construct tables from structured reasoning, not from raw merged text.

FORMAT RULES:
Tables MUST follow valid markdown:

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Row A    | Value    | Notes    |

ALLOWED BEHAVIOR:
- If the merged source contains messy or repeated lines,
  CLEAN them before producing the table.
- You may infer missing descriptions using domain knowledge,
  BUT must stay within topic boundaries.

FORBIDDEN:
- Do NOT echo raw source lines inside table columns.
- Do NOT generate malformed markdown.

If the topic does not need a table, simply skip this section.

## 5. Components / Architecture / Roles
- List components/modules/actors if applicable.
- Explain each one's role and how they interact.

## 6. Examples
Choose the best example type for the topic:
- Code snippets (for programming topics),
- ASCII diagrams (for structures/architectures),
- Real-world scenarios (for conceptual topics),
- Small numeric examples (for math-related topics).

## 7. Key Principles / Rules / Theorems / Formulas
- Summarize important rules or formulas mentioned or strongly implied.
- Briefly explain each in plain language.

## 8. Applications & Use Cases
- Describe where and how the topic is applied in real systems or problems.

## 9. Summary Sheet (Quick Revision)
- 10–15 bullet points that capture the main ideas of the entire guide.
- This section should stand alone as a quick revision sheet.

====================================================
RAW SOURCE CONTENT (MERGED)
====================================================
{safe_context}
====================================================

Now generate the complete Master Study Guide.
"""

    return client.generate_text(prompt, system_prompt=system_prompt)


# ---------------------------------------------------------------------------
# 4. HIGH-LEVEL HELPERS
# ---------------------------------------------------------------------------

def generate_study_guide_from_url(url: str, topic: str, max_pages: int = 15) -> str:
    """
    Full Option C pipeline:
    1. Crawl the site starting from `url` (same domain, up to `max_pages`).
    2. Merge all extracted text.
    3. Feed into `generate_learning_content`.
    """
    merged_text = crawl_and_merge(root_url=url, max_pages=max_pages, same_domain=True)

    if not merged_text.strip():
        return (
            f"Failed to extract enough content from {url}. "
            "Check the URL or increase max_pages."
        )

    return generate_learning_content(context=merged_text, topic=topic, mode="study_guide")


def generate_study_guide_from_text(text: str, topic: str) -> str:
    """
    Convenience wrapper if you already have raw text
    (e.g. from a PDF extractor).
    """
    return generate_learning_content(context=text, topic=topic, mode="study_guide")
