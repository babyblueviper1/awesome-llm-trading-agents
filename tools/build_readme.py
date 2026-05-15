#!/usr/bin/env python3
"""Render README.md deterministically from entries/**/*.yaml.

Usage:
  python tools/build_readme.py          # write README.md
  python tools/build_readme.py --check  # exit 1 if README.md is stale
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
ENTRIES = REPO_ROOT / "entries"
TEMPLATE = Path(__file__).resolve().parent / "README.template.md"
OUTPUT = REPO_ROOT / "README.md"

SECTION_TITLES = {
    "01-frameworks": "Multi-Agent LLM Trading Frameworks",
    "02-single-agent": "Single-Agent & Memory-Augmented LLM Traders",
    "03-papers": "Foundational & Influential Papers",
    "04-datasets": "Financial Datasets",
    "05-benchmarks": "Benchmarks & Evaluations",
    "06-backtesting": "Backtesting & Execution Infrastructure",
    "07-simulators": "Market-Simulation Environments",
    "08-related-lists": "Related Lists",
}

SECTION_BLURB = {
    "01-frameworks": "End-to-end LLM-agent systems for trading or investment decisions. The 73k-star anchor of the field lives here.",
    "02-single-agent": "Single-LLM or memory-augmented traders that don't coordinate a team of agents. Often the cleanest substrate for ablation studies.",
    "03-papers": "Foundational papers, surveys, and recent work on the methodology, biases, and limits of LLM trading systems.",
    "04-datasets": "Data sources used to train, evaluate, or backtest LLM trading agents.",
    "05-benchmarks": "Held-out evaluations. The category most worth reading critically — many benchmarks are easy to game without external validity.",
    "06-backtesting": "Backtesting and execution engines. None are LLM-specific; all are essential plumbing for honest evaluation.",
    "07-simulators": "Agent-based market simulators — the substrate for studying multi-agent dynamics without live-market risk.",
    "08-related-lists": "Other awesome lists that border this one. Link generously, scope tightly.",
}


def load_entries() -> list[dict]:
    items: list[dict] = []
    for path in sorted(ENTRIES.rglob("*.yaml")):
        with path.open("r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        if not data:
            continue
        if data.get("verification", {}).get("status") != "verified":
            continue
        items.append(data)
    return items


def sort_key(entry: dict):
    stars = (entry.get("metrics") or {}).get("stars") or 0
    year = entry.get("year") or 0
    return (entry.get("subcategory") or "zz", -stars, -year, entry.get("title", "").lower())


def fmt_stars(n) -> str:
    if not isinstance(n, (int, float)) or n <= 0:
        return ""
    if n >= 1000:
        return f"{n/1000:.1f}k★"
    return f"{int(n)}★"


def cell_escape(s: str) -> str:
    return (s or "").replace("|", "\\|").replace("\n", " ").strip()


def render_section(category: str, entries: list[dict]) -> str:
    title = SECTION_TITLES[category]
    blurb = SECTION_BLURB[category]
    lines = [f"## {title}", "", blurb, ""]
    if not entries:
        lines += ["_No entries yet._", ""]
        return "\n".join(lines)

    lines.append("| Project / Paper | Type | Year / Stars | What it is | Honest note |")
    lines.append("|---|---|---|---|---|")
    for e in sorted(entries, key=sort_key):
        link = f"[{e['title']}]({e['url']})"
        if e.get("paper_url") and e["paper_url"] != e["url"]:
            link += f" · [paper]({e['paper_url']})"
        type_cell = e["type"]
        metrics = e.get("metrics") or {}
        meta_parts = []
        if e.get("year"):
            meta_parts.append(str(e["year"]))
        stars_str = fmt_stars(metrics.get("stars"))
        if stars_str:
            as_of = metrics.get("as_of")
            meta_parts.append(stars_str + (f" ({as_of})" if as_of else ""))
        meta_cell = " / ".join(meta_parts) or "—"
        desc = cell_escape(e["description"])
        note = cell_escape(e["note"])
        lines.append(f"| {link} | {type_cell} | {meta_cell} | {desc} | {note} |")
    lines.append("")
    return "\n".join(lines)


def render(template: str, entries: list[dict]) -> str:
    by_cat: dict[str, list[dict]] = {c: [] for c in SECTION_TITLES}
    for e in entries:
        by_cat.setdefault(e["category"], []).append(e)

    body_parts: list[str] = []
    for cat in SECTION_TITLES:
        body_parts.append(render_section(cat, by_cat.get(cat, [])))

    toc = "\n".join(f"- [{SECTION_TITLES[c]}](#{slug_anchor(SECTION_TITLES[c])})" for c in SECTION_TITLES)
    toc += "\n- [Methodology & Common Pitfalls](docs/methodology.md)"
    toc += "\n- [Contributing](CONTRIBUTING.md)"
    toc += "\n- [Curator & License](#curator--license)"

    total = sum(len(v) for v in by_cat.values())
    output = template
    output = output.replace("{{TOC}}", toc)
    output = output.replace("{{BODY}}", "\n".join(body_parts))
    output = output.replace("{{TOTAL_ENTRIES}}", str(total))
    return output


def slug_anchor(s: str) -> str:
    return (
        s.lower()
        .replace("&", "")
        .replace("/", "")
        .replace(",", "")
        .replace("(", "")
        .replace(")", "")
        .replace(":", "")
        .strip()
        .replace("  ", " ")
        .replace(" ", "-")
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="exit 1 if README is stale")
    args = parser.parse_args()

    if not TEMPLATE.exists():
        print(f"missing template: {TEMPLATE}", file=sys.stderr)
        return 1
    template = TEMPLATE.read_text(encoding="utf-8")
    entries = load_entries()
    rendered = render(template, entries)

    if args.check:
        current = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""
        if current.strip() != rendered.strip():
            print("README.md is out of date. Run: python tools/build_readme.py", file=sys.stderr)
            return 1
        print("README.md is up to date.")
        return 0

    OUTPUT.write_text(rendered, encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(REPO_ROOT)} from {len(entries)} verified entries.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
