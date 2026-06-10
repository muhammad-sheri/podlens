"""Claude-powered analytics insights.

This is the integration structure for Phase 1. It is gated on ANTHROPIC_API_KEY:
when no key is configured the app returns a clearly-labeled canned insight so the
whole product runs locally with zero credentials. Set ANTHROPIC_API_KEY to switch
to live Claude-generated insights — no other code changes required.
"""
import json

from django.conf import settings

MODEL = "claude-opus-4-8"

SYSTEM_PROMPT = (
    "You are a podcast analytics advisor. Given summary statistics for a "
    "creator's shows, produce 3-5 concise, concrete, actionable insights about "
    "performance trends, platform mix, and audience retention. Be specific and "
    "reference the numbers. Avoid generic filler."
)


def _stub_insight(summary_stats: dict) -> str:
    totals = summary_stats.get("totals", {})
    platforms = summary_stats.get("platforms", [])
    top = max(platforms, key=lambda p: p.get("downloads", 0), default=None)
    lines = [
        "[STUB INSIGHT — set ANTHROPIC_API_KEY to enable live Claude analysis]",
        "",
        f"- Across the last 90 days you logged {totals.get('downloads', 0):,} "
        f"downloads and {totals.get('listeners', 0):,} unique listeners.",
        f"- Average retention sits at {totals.get('avg_retention', 0)}% — "
        "episodes that open with a strong hook tend to lift this.",
    ]
    if top:
        lines.append(
            f"- {top['platform'].title()} is your strongest platform by downloads "
            f"({top['downloads']:,}). Consider doubling down on its discovery features."
        )
    lines.append(
        "- Publishing cadence and cross-promotion are the usual next levers once "
        "retention is healthy."
    )
    return "\n".join(lines)


def generate_insight(summary_stats: dict) -> dict:
    """Return {'source': 'claude'|'stub', 'text': str}."""
    if not settings.ANTHROPIC_API_KEY:
        return {"source": "stub", "text": _stub_insight(summary_stats)}

    # Live path — only imported/exercised when a key is present.
    import anthropic

    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    message = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        thinking={"type": "adaptive"},
        output_config={"effort": "medium"},
        messages=[
            {
                "role": "user",
                "content": (
                    "Here are the podcast analytics summary statistics as JSON. "
                    "Give me your insights:\n\n"
                    + json.dumps(summary_stats, indent=2)
                ),
            }
        ],
    )
    text = next((b.text for b in message.content if b.type == "text"), "")
    return {"source": "claude", "text": text}
